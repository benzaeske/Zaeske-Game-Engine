import copy
from typing import Tuple, Callable
from uuid import UUID

from pygame import Vector2, Rect
from pygame.key import ScancodeWrapper

from model.entitygroups.entitygroupv1 import EntityGroupV1
from model.entities.gameentity import GameEntity
from model.spawners.spawner import Spawner
from model.world.entitymanagerindex import EntityManagerIndex
from model.world.entitymanagerv1 import EntityManagerV1
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
        self.entity_manager: EntityManagerV1 = EntityManagerV1()
        self.spawners: dict[UUID, Spawner] = {}
        self.player: Player = player

    # ------- Refactor access functions --------
    def add_entity_group(self, entity_group: EntityGroupV1) -> None:
        self.entity_manager.add_entity_group(entity_group)

    def remove_entity_group(self, group_id: UUID) -> None:
        self.entity_manager.remove_entity_group(group_id)

    def add_spawner(self, spawner: Spawner) -> None:
        self.spawners[spawner.spawner_id] = spawner

    def remove_spawner(self, spawner_id: UUID) -> None:
        self.spawners.pop(spawner_id, None)

    # --------- Refactor Update Functions -----------

    def update_model(self, dt: float, key_presses: ScancodeWrapper, score_callback: Callable[[int], None]) -> None:
        self.process_spawners(dt)
        self.update_entity_groups()
        self.update_player(dt, key_presses, score_callback)
        self.move_entity_groups(dt)
        self.move_player(dt, key_presses)

    def process_spawners(self, dt: float) -> None:
        """
        Tick each spawner's cooldown and perform the spawn function if it returns true
        """
        for spawner_id in list(self.spawners.keys()):
            spawner: Spawner = self.spawners[spawner_id]
            if spawner.tick_spawn_timer(dt):
                spawner.spawn(self.grid_space, self.world_specs, self.player.camera_specs, Vector2(self.player.camera.center))
            if spawner.should_destroy():
                self.remove_spawner(spawner_id)

    def update_player(self, dt: float, key_presses: ScancodeWrapper, score_callback: Callable[[int], None]) -> None:
        """
        - Calculate acceleration based on key presses and input events
        - update current state based on neighbor entities
        """
        # TODO make player move using velocity/acceleration
        self.process_player_fish_coherency(dt)
        self.process_player_jelly_collisions(dt)
        # TODO Process deleted entities when updating them instead of in the item
        self.update_player_items(score_callback)

    def process_player_fish_coherency(self, dt: float) -> None:
        # Player's grid space coordinate
        p_coord: Tuple[int, int] = self.grid_space.get_grid_cell_coord_from_position(self.player.position.x, self.player.position.y)
        # Player's grid cell
        p_grid_cell: GridCell = self.grid_space.get_grid_cell(p_coord)
        # Set coherence amounts on player so other functions can reference it quickly
        self.player.cohere_red = len(
            p_grid_cell.get_entities_by_group_ids_v1(
                self.entity_manager.get_group_ids_by_type(EntityManagerIndex.RED_FISH)
            )
        )
        self.player.cohere_yellow = len(
            p_grid_cell.get_entities_by_group_ids_v1(
                self.entity_manager.get_group_ids_by_type(EntityManagerIndex.YELLOW_FISH)
            )
        )
        self.player.cohere_green = len(
            p_grid_cell.get_entities_by_group_ids_v1(
                self.entity_manager.get_group_ids_by_type(EntityManagerIndex.GREEN_FISH)
            )
        )
        # Process immediate coherence effects
        self.player.update_hp(1 * dt * self.player.cohere_green)
        if self.player.cohere_yellow > 0:
            self.player.charge_shield(dt)

    def process_player_jelly_collisions(self, dt: float) -> None:
        cell_range: int = 1
        # Only process collisions for jellies that are within a cell range that can actually reach the player
        r: int = int(self.player.position.y / self.world_specs.cell_size)
        c: int = int(self.player.position.x / self.world_specs.cell_size)
        # Get all jelly group ids to use for easy querying later
        jelly_group_ids: set[UUID] = self.entity_manager.get_group_ids_by_type(EntityManagerIndex.JELLY)
        for dr in range(-cell_range, cell_range + 1):
            for dc in range(-cell_range, cell_range + 1):
                grid_r: int = r + dr
                grid_r = (grid_r + self.world_specs.grid_height) % self.world_specs.grid_height
                # Virtual grid column is the column before wrapping
                virtual_grid_c: int = c + dc
                # Grid column wrapped to fit in grid boundary
                grid_c: int = (virtual_grid_c + self.world_specs.grid_width) % self.world_specs.grid_width
                # The current grid cell
                gc: GridCell = self.grid_space.get_grid_cell((grid_r, grid_c))
                for jelly in gc.get_entities_by_group_ids_v1(jelly_group_ids):
                    jelly_hitbox: Rect = jelly.hitbox
                    if virtual_grid_c < 0 or virtual_grid_c >= self.world_specs.grid_width:
                        jelly_hitbox = self.get_virtual_wrapped_hitbox(jelly, virtual_grid_c)
                    if jelly_hitbox.colliderect(self.player.hitbox):
                        self.player.health -= jelly.damage * dt


    def update_player_items(self, score_callback: Callable[[int], None]) -> None:
        # TODO create an abstract Item class with an update method. Track items globally
        self.shield_update(score_callback)

    def shield_update(self, score_callback: Callable[[int], None]):
        # TODO Move to the 'Shield' Item impl once Item is an abstract class
        if self.player.shield > 0:
            # Only process shield collisions for jellies that are within a cell range that can actually reach the player shield
            shield_cell_range: int = 2
            # Get the grid cell row/column of the player's current position
            r: int = int(self.player.position.y / self.world_specs.cell_size)
            c: int = int(self.player.position.x / self.world_specs.cell_size)
            # Get all jelly group ids to use for easy querying later
            jelly_group_ids: set[UUID] = self.entity_manager.get_group_ids_by_type(EntityManagerIndex.JELLY)
            for dr in range(-shield_cell_range, shield_cell_range + 1):
                for dc in range(-shield_cell_range, shield_cell_range + 1):
                    grid_r: int = r + dr
                    grid_r = (grid_r + self.world_specs.grid_height) % self.world_specs.grid_height
                    # Virtual grid column is the column before wrapping
                    virtual_grid_c: int = c + dc
                    # Grid column wrapped to fit in grid boundary
                    grid_c: int = (virtual_grid_c + self.world_specs.grid_width) % self.world_specs.grid_width
                    # The current grid cell
                    gc: GridCell = self.grid_space.get_grid_cell((grid_r, grid_c))
                    for jelly in gc.get_entities_by_group_ids_v1(jelly_group_ids):
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
                            # TODO delete jellies when health reaches 0 instead of shield killing them instantly
                            self.player.decrement_shield()
                            self.entity_manager.remove_entity(jelly)
                            self.grid_space.remove_entity_v1(jelly)
                            # Note: This is in the item's update method right now since the item is erasing the enemies directly from the game. Eventually this should
                            # be moved to wherever entity 'death' handling is done
                            score_callback(1)

    def update_entity_groups(self) -> None:
        """
        - individual entities may decide how to move themselves
        - entities may act on other entities
        - checking entity hp to determine if they should be removed because they 'died' should be done here
        """
        self.entity_manager.update_all_groups(self.grid_space, self.world_specs, self.player.position)

    def move_entity_groups(self, dt: float) -> None:
        """
        Before calling this each frame:\n
        - All updates to each entity's self-imposed acceleration have been made
        - All relevant external forces have been applied to each entity
        - Entities that were killed this frame have been removed
        """
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
