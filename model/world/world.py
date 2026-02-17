import copy
from typing import Tuple
from uuid import UUID

from pygame import Vector2, Rect
from pygame.key import ScancodeWrapper

from model.entitygroups.entitygroup import EntityGroup
from model.entities.fish.fish import Fish
from model.entities.fish.fishsettings import FishType
from model.entities.gameentity import GameEntity
from model.entitygroups.jellyfishswarm.jellyfishswarm import JellyfishSwarm
from model.entitygroups.school.school import School
from model.spawners.spawner import Spawner
from model.world.entitymanager import EntityManager
from model.world.gridspace import GridSpace
from model.player.player import Player
from model.world.grid_cell import GridCell
from model.world.worldspecs import WorldSpecs


class SpatialPartitioningModel:
    def __init__(
        self,
        world_specs: WorldSpecs,
        player: Player,
    ):
        self.world_specs: WorldSpecs = world_specs
        self.grid_space: GridSpace = GridSpace(world_specs)
        self.entity_manager: EntityManager = EntityManager()
        self.spawners: dict[UUID, Spawner] = {}
        self.player: Player = player

    # ------- Refactor access functions --------
    def add_entity_group(self, entity_group: EntityGroup) -> None:
        self.entity_manager.add_entity_group(entity_group)

    def remove_entity_group(self, group_id: UUID) -> None:
        self.entity_manager.remove_entity_group(group_id)

    def add_spawner(self, spawner: Spawner) -> None:
        self.spawners[spawner.spawner_id] = spawner

    def remove_spawner(self, spawner_id: UUID) -> None:
        self.spawners.pop(spawner_id, None)

    # --------- Refactor Update Functions -----------

    def update_model(self, dt: float, key_presses: ScancodeWrapper) -> None:
        # Process spawners (decrement cooldown, spawn if ready)
        self.process_spawners(dt)
        # Update player (update current state based on entity proximity; check collisions etc.)
        # Update player items (Items can interact with entities in the world space or with the player)
        self.update_player(dt, key_presses)
        # Update entity groups (Decisions that each entity makes on their own based on their environment)
        self.update_entity_groups()
        # Move entity groups
        self.move_entity_groups(dt)
        # Move player
        self.move_player(dt, key_presses)
        pass

    def process_spawners(self, dt: float) -> None:
        """
        Tick each spawner's cooldown and perform the spawn function if it returns true
        """
        for spawner_id in self.spawners.keys():
            spawner: Spawner = self.spawners[spawner_id]
            if spawner.tick_spawn_timer(dt):
                spawner.spawn(self.grid_space, Vector2(self.player.camera.center))
            if spawner.should_destroy():
                self.remove_spawner(spawner_id)

    def update_player(self, dt: float, key_presses: ScancodeWrapper) -> None:
        # TODO make player move using velocity/acceleration
        self.process_player_fish_coherency(dt)
        self.process_player_jelly_collisions(dt)
        self.update_player_items()

    def process_player_fish_coherency(self, dt: float) -> None:
        # Track number of fish types in player's grid cell
        cohere_red: int = 0
        cohere_green: int = 0
        cohere_yellow: int = 0
        # Player's grid space coordinate
        p_coord: Tuple[int, int] = self.grid_space.get_grid_cell_coord_from_position(self.player.position.x, self.player.position.y)
        # Player's grid cell
        p_grid_cell: GridCell = self.grid_space.get_grid_cell(p_coord)
        for group_id, entities in p_grid_cell.contained_entities_by_group.items():
            eg: EntityGroup = self.entity_manager.get_entity_group(group_id)
            if isinstance(eg, School):
                match eg.fish_settings.fish_type:
                    case FishType.RED:
                        cohere_red += len(entities)
                    case FishType.GREEN:
                        cohere_green += len(entities)
                    case FishType.YELLOW:
                        cohere_yellow += len(entities)
        # Set coherence amounts on player so other functions can reference it quickly
        self.player.cohere_green = cohere_green
        self.player.cohere_yellow = cohere_yellow
        self.player.cohere_green_red = cohere_red
        # Process immediate coherence effects
        self.player.update_hp(1 * dt * cohere_green)
        if cohere_yellow > 0:
            self.player.charge_shield(dt)

    def process_player_jelly_collisions(self, dt: float) -> None:
        cell_range: int = 1
        # Only process collisions for jellies that are within a cell range that can actually reach the player
        r: int = int(self.player.position.y / self.world_specs.cell_size)
        c: int = int(self.player.position.x / self.world_specs.cell_size)
        for dr in range(-cell_range, cell_range + 1):
            for dc in range(-cell_range, cell_range + 1):
                grid_r: int = r + dr
                grid_r = (grid_r + self.world_specs.grid_height) % self.world_specs.grid_height
                # Virtual grid column is used for world-wrapping calculations
                virtual_grid_c: int = c + dc
                grid_c: int = (virtual_grid_c + self.world_specs.grid_width) % self.world_specs.grid_width
                gc: GridCell = self.grid_space.get_grid_cell((grid_r, grid_c))
                for group_id, entities in gc.contained_entities_by_group.items():
                    eg: EntityGroup = self.entity_manager.get_entity_group(group_id)
                    if isinstance(eg, JellyfishSwarm):
                        for jelly in entities:
                            jelly_hitbox: Rect = jelly.hitbox
                            if virtual_grid_c < 0 or virtual_grid_c >= self.world_specs.grid_width:
                                jelly_hitbox = self.get_virtual_wrapped_hitbox(jelly, virtual_grid_c)
                            if jelly_hitbox.colliderect(self.player.hitbox):
                                self.player.health -= jelly.damage * dt

    def update_player_items(self) -> None:
        # TODO create an abstract Item class with an update method. Track items globally
        self.shield_update()

    def shield_update(self):
        # TODO Move to the 'Shield' Item impl once Item is an abstract class
        if self.player.shield > 0:
            shield_cell_range: int = 2
            # Only process shield collisions for jellies that are within a cell range that can actually reach the player shield
            r: int = int(self.player.position.y / self.world_specs.cell_size)
            c: int = int(self.player.position.x / self.world_specs.cell_size)
            for dr in range(-shield_cell_range, shield_cell_range + 1):
                for dc in range(-shield_cell_range, shield_cell_range + 1):
                    grid_r: int = r + dr
                    grid_r = (grid_r + self.world_specs.grid_height) % self.world_specs.grid_height
                    # Track virtual grid column needed for wrapping calculations.
                    virtual_grid_c: int = c + dc
                    grid_c: int = (virtual_grid_c + self.world_specs.grid_width) % self.world_specs.grid_width
                    gc: GridCell = self.grid_space.get_grid_cell((grid_r, grid_c))
                    for group_id, entities in gc.contained_entities_by_group.items():
                        eg: EntityGroup = self.entity_manager.get_entity_group(group_id)
                        if isinstance(eg, JellyfishSwarm):
                            # Track entities that need to be deleted because they touched the shield
                            remove_entities: list[GameEntity] = []
                            for jelly in entities:
                                jelly_hitbox: Rect = jelly.hitbox
                                if virtual_grid_c < 0 or virtual_grid_c >= self.world_specs.grid_width:
                                    jelly_hitbox = self.get_virtual_wrapped_hitbox(jelly, virtual_grid_c)
                                # find the closest point on the jelly's hitbox to the player's circular shield
                                closest_point: Vector2 = Vector2(
                                    max(
                                        jelly_hitbox.left,
                                        min(int(self.player.position.x), jelly_hitbox.right),
                                    ),
                                    max(
                                        jelly_hitbox.top,
                                        min(int(self.player.position.y), jelly_hitbox.bottom),
                                    ),
                                )
                                if closest_point.distance_squared_to(self.player.position) < self.player.shield_radius_squared:
                                    self.player.decrement_shield()
                                    remove_entities.append(jelly)
                            for entity in remove_entities:
                                self.entity_manager.remove_entity(entity)
                                self.grid_space.remove_entity(entity)

    def update_entity_groups(self) -> None:
        self.entity_manager.update_all_groups(self.grid_space, self.world_specs, self.player.position)

    def move_entity_groups(self, dt: float) -> None:
        self.entity_manager.move_all_groups(self.grid_space, self.world_specs, dt)

    def move_player(self, dt: float, key_presses: ScancodeWrapper):
        # TODO make player move using velocity/acceleration
        self.player.move_player(key_presses, dt)

    #--------- Helper functions -----------

    def get_virtual_wrapped_hitbox(
        self, game_entity: GameEntity, virtual_grid_r: int
    ) -> Rect:
        virtual_hitbox: Rect = copy.deepcopy(game_entity.hitbox)
        if virtual_grid_r < 0:
            virtual_hitbox.center = (
                int(game_entity.position.x - self.world_specs.world_width),
                int(game_entity.position.y),
            )
        elif virtual_grid_r >= self.world_specs.grid_width:
            virtual_hitbox.center = (
                int(game_entity.position.x + self.world_specs.world_width),
                int(game_entity.position.y),
            )
        return virtual_hitbox
