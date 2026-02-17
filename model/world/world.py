import copy
import random
from typing import Tuple
from uuid import UUID

import pygame
from pygame import Surface, Vector2, Rect
from pygame.key import ScancodeWrapper

from model.entitygroups.entitygroup import EntityGroup
from model.entities.fish.fish import Fish
from model.entities.fish.fishsettings import FishType
from model.entities.gameentity import GameEntity
from model.entities.jellyfish.jellyfish import Jellyfish
from model.entitygroups.jellyfishswarm.jellyfishswarm import JellyfishSwarm
from model.entitygroups.school.school import School
from model.spawners.spawner import Spawner
from model.world.entitymanager import EntityManager
from model.world.gridspace import GridSpace
from model.player.player import Player
from model.world.grid_cell import GridCell
from model.world.worldspecs import WorldSpecs


class SpatialPartitioningModel:
    """
    Implementation of spatial partitioning. The 'world' is divided into a grid of cells. The size of a cell determines how far entities in the simulation can 'see'.\n
    When applying the schooling algorithm to fish, calculations are only performed on neighbors within the fish's cell and the cells surrounding it as defined by a variable cell detection radius.\n
    For V1, The world width and height must be evenly divisible by cell_size, or array out of bounds issues will occur\n
    """

    def __init__(
        self,
        world_specs: WorldSpecs,
        player: Player,
    ):
        # Old stuff
        self.schools: dict[UUID, School] = {}
        self.jellyfish_spawner: JellyfishSwarm | None = None
        self.jelly_spawner_delay: float = 10.0
        self.jelly_spawner_timer: float = 0.0
        self.grid_space_old: list[list[GridCell]] = self.initialize_grid_space_old()
        self.fish: dict[UUID, Fish] = {}
        self.jellyfish: dict[UUID, Jellyfish] = {}
        self.entity_groups: dict[UUID, EntityGroup] = {}

        # Refactor
        self.world_specs: WorldSpecs = world_specs
        self.grid_space: GridSpace = GridSpace(
            world_specs.grid_width,
            world_specs.grid_height,
            world_specs.cell_size
        )
        self.entity_manager: EntityManager = EntityManager()
        self.spawners: dict[UUID, Spawner] = {}
        self.player: Player = player

    # Refactor functions
    def add_entity_group(self, entity_group: EntityGroup) -> None:
        self.entity_manager.add_entity_group(entity_group)

    def remove_entity_group(self, group_id: UUID) -> None:
        self.entity_manager.remove_entity_group(group_id)

    def add_spawner(self, spawner: Spawner) -> None:
        self.spawners[spawner.spawner_id] = spawner

    def remove_spawner(self, spawner_id: UUID) -> None:
        self.spawners.pop(spawner_id, None)

    def update_model_new(self, dt: float, key_presses: ScancodeWrapper) -> None:
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
        for spawner in self.spawners.values():
            if spawner.tick_spawn_timer(dt):
                spawner.spawn(self.grid_space, Vector2(self.player.camera.center))

    def update_player(self, dt: float, key_presses: ScancodeWrapper) -> None:
        # TODO make player move using velocity/acceleration
        # TODO update the below functions for the refactor
        self.process_player_fish_coherency(dt)
        self.process_player_jelly_collisions_old(dt)
        # TODO items
        self.update_player_items()

    def update_entity_groups(self) -> None:
        self.entity_manager.update_all_groups(self.grid_space, self.world_specs, self.player.position)

    def update_player_items(self) -> None:
        pass

    def move_entity_groups(self, dt: float) -> None:
        self.entity_manager.move_all_groups(self.grid_space, self.world_specs, dt)

    def move_player(self, dt: float, key_presses: ScancodeWrapper):
        # TODO make player move using velocity/acceleration
        self.player.move_player(key_presses, dt)

    def initialize_grid_space_old(self) -> list[list[GridCell]]:
        grid_space: list[list[GridCell]] = []
        for row in range(self.world_specs.grid_height):
            grid_space.append([])
            for col in range(self.world_specs.grid_width):
                background: Surface = pygame.Surface(
                    (
                        self.world_specs.cell_size,
                        self.world_specs.cell_size,
                    )
                )
                noise: int = random.randint(0, 25)
                if row == 0:
                    background.fill((99, 85, 52))
                else:
                    background.fill((0, 50 + noise, 115 + noise * 2))
                grid_space[row].append(
                    GridCell((row, col), background)
                )
        return grid_space

    def add_entity_group_old(self, entity_group: EntityGroup) -> None:
        self.entity_groups[entity_group.group_id] = entity_group

    def hatch_schools_old(self):
        for school in self.schools.values():
            for _ in range(school.school_params.egg_count):
                self.spawn_fish_in_grid_space(school.hatch_fish())

    def update_model_old(self, dt: float, key_presses: ScancodeWrapper) -> None:
        self.update_player_old(dt)
        self.update_fish(dt)
        self.spawn_jellyfish(dt)
        self.update_jellyfish(dt)
        self.player.move_player(key_presses, dt)

    def update_player_old(self, dt: float) -> None:
        self.process_player_fish_coherency_old(dt)
        self.process_player_jelly_collisions_old(dt)

    def process_player_fish_coherency_old(self, dt: float) -> None:
        r: int = int(self.player.position.y / self.world_specs.cell_size)
        c: int = int(self.player.position.x / self.world_specs.cell_size)
        cohere_red: int = 0
        cohere_green: int = 0
        cohere_yellow: int = 0
        for fish in self.grid_space_old[r][c].fish.values():
            match self.schools.get(fish.group_id).fish_settings.fish_type:
                case FishType.RED:
                    cohere_red += 1
                case FishType.GREEN:
                    cohere_green += 1
                case FishType.YELLOW:
                    cohere_yellow += 1
        # Set coherence amounts on player so other functions can reference it quickly
        self.player.cohere_green = cohere_green
        self.player.cohere_yellow = cohere_yellow
        self.player.cohere_green_red = cohere_red
        # Process immediate coherence effects
        self.player.update_hp(1 * dt * cohere_green)
        if cohere_yellow > 0:
            self.player.charge_shield(dt)

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

    def process_player_jelly_collisions_old(self, dt: float) -> None:
        cell_range: int = 1
        # Only process collisions for jellies that are within a cell range that can actually reach the player
        r: int = int(self.player.position.y / self.world_specs.cell_size)
        c: int = int(self.player.position.x / self.world_specs.cell_size)
        for dr in range(-cell_range, cell_range + 1):
            for dc in range(-cell_range, cell_range + 1):
                grid_r: int = r + dr
                grid_r = (
                    grid_r + self.world_specs.grid_height
                ) % self.world_specs.grid_height
                virtual_grid_c: int = c + dc
                grid_c: int = (
                    virtual_grid_c + self.world_specs.grid_width
                ) % self.world_specs.grid_width
                for jelly in self.grid_space_old[grid_r][grid_c].jellyfish.values():
                    jelly_hitbox: Rect = jelly.hitbox
                    if (
                        virtual_grid_c < 0
                        or virtual_grid_c >= self.world_specs.grid_width
                    ):
                        jelly_hitbox = self.get_virtual_wrapped_hitbox(
                            jelly, virtual_grid_c
                        )
                    if jelly_hitbox.colliderect(self.player.hitbox):
                        self.player.health -= jelly.damage * dt

    ##############################
    ######## Fish functions ######
    ##############################

    def add_school(self, school: School) -> None:
        self.schools[school.school_id] = school

    def spawn_fish_in_grid_space(self, new_fish: Fish) -> None:
        self.fish[new_fish.entity_id] = new_fish
        self.grid_space_old[int(new_fish.position.y / self.world_specs.cell_size)][
            int(new_fish.position.x / self.world_specs.cell_size)
        ].fish[new_fish.entity_id] = new_fish

    def update_fish(self, dt: float):
        # Have all the fish make schooling decisions based on their current location and velocity
        for current_fish in self.fish.values():
            self.find_neighbors_and_make_schooling_decisions(current_fish)
        # Move all the fish: this should only be done after all schooling decisions have been made for the current frame
        for current_fish in self.fish.values():
            old_r = int(current_fish.position.y / self.world_specs.cell_size)
            old_c = int(current_fish.position.x / self.world_specs.cell_size)
            current_fish.update_position(
                self.world_specs.world_width,
                self.world_specs.world_height,
                dt,
            )
            # Check if we are in a new grid cell after moving
            new_r = int(current_fish.position.y / self.world_specs.cell_size)
            new_c = int(current_fish.position.x / self.world_specs.cell_size)
            if new_r != old_r or new_c != old_c:
                del self.grid_space_old[old_r][old_c].fish[current_fish.entity_id]
                self.grid_space_old[new_r][new_c].fish[current_fish.entity_id] = current_fish

    def find_neighbors_and_make_schooling_decisions(self, current_fish: Fish) -> None:
        """
        Finds this entity's relevant neighbors and applies the schooling algorithm using only the list of relevant neighbors
        """
        school: School = self.schools[current_fish.group_id]
        cell_range: int = school.school_params.interaction_cell_range
        neighbors: list[Fish] = []
        r: int = int(current_fish.position.y / self.world_specs.cell_size)
        c: int = int(current_fish.position.x / self.world_specs.cell_size)
        for dr in range(-cell_range, cell_range + 1):
            for dc in range(-cell_range, cell_range + 1):
                grid_r: int = r + dr
                grid_r = (
                    grid_r + self.world_specs.grid_height
                ) % self.world_specs.grid_height
                grid_c: int = c + dc
                grid_c = (
                    grid_c + self.world_specs.grid_width
                ) % self.world_specs.grid_width
                neighbors.extend(self.grid_space_old[grid_r][grid_c].fish.values())
        current_fish.make_schooling_decisions(
            neighbors,
            school.school_params,
            self.world_specs.world_width,
            self.world_specs.world_height,
        )

    ##############################
    ##### Jellyfish functions ####
    ##############################

    def set_jellyfish_spawner(self, spawner: JellyfishSwarm) -> None:
        self.jellyfish_spawner = spawner

    def spawn_jellyfish(self, dt: float):
        self.jelly_spawner_timer -= dt
        if self.jelly_spawner_timer <= 0:
            for _ in range(self.jellyfish_spawner.amount):
                # create the jelly from the spawner
                new_jelly: Jellyfish = self.jellyfish_spawner.spawn_jellyfish(
                    self.player.position,
                    self.player.camera_w_adjust,
                    self.player.camera_h_adjust,
                    self.world_specs.world_width,
                    self.world_specs.world_height,
                )
                self.jellyfish[new_jelly.entity_id] = new_jelly
                self.grid_space_old[
                    int(new_jelly.position.y / self.world_specs.cell_size)
                ][
                    int(new_jelly.position.x / self.world_specs.cell_size)
                ].jellyfish[
                    new_jelly.entity_id
                ] = new_jelly
            # reset jelly spawn timer
            self.jelly_spawner_timer = self.jelly_spawner_delay
            self.jellyfish_spawner.amount += 1

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

    def update_jellyfish(self, dt: float):
        if self.player.shield > 0:
            shield_cell_range: int = 2
            # Only process shield collisions for jellies that are within a cell range that can actually reach the player shield
            r: int = int(self.player.position.y / self.world_specs.cell_size)
            c: int = int(self.player.position.x / self.world_specs.cell_size)
            for dr in range(-shield_cell_range, shield_cell_range + 1):
                for dc in range(-shield_cell_range, shield_cell_range + 1):
                    grid_r: int = r + dr
                    grid_r = (
                        grid_r + self.world_specs.grid_height
                    ) % self.world_specs.grid_height
                    virtual_grid_c: int = c + dc
                    grid_c: int = (
                        virtual_grid_c + self.world_specs.grid_width
                    ) % self.world_specs.grid_width
                    for jelly_id in list(
                        self.grid_space_old[grid_r][grid_c].jellyfish.keys()
                    ):
                        jelly = self.grid_space_old[grid_r][grid_c].jellyfish[jelly_id]
                        jelly_hitbox: Rect = jelly.hitbox
                        if (
                            virtual_grid_c < 0
                            or virtual_grid_c >= self.world_specs.grid_width
                        ):
                            jelly_hitbox = self.get_virtual_wrapped_hitbox(
                                jelly, virtual_grid_c
                            )
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
                        if (
                            closest_point.distance_squared_to(self.player.position)
                            < self.player.shield_radius_squared
                        ):
                            self.player.decrement_shield()
                            del self.jellyfish[jelly_id]
                            del self.grid_space_old[grid_r][grid_c].jellyfish[jelly_id]

        neighbor_range: int = 1
        scared_range: int = 2
        for jellyfish in self.jellyfish.values():
            neighbor_jellies: list[Jellyfish] = []
            r: int = int(jellyfish.position.y / self.world_specs.cell_size)
            c: int = int(jellyfish.position.x / self.world_specs.cell_size)
            for dr in range(-neighbor_range, neighbor_range + 1):
                for dc in range(-neighbor_range, neighbor_range + 1):
                    grid_r: int = r + dr
                    grid_r = (
                        grid_r + self.world_specs.grid_height
                    ) % self.world_specs.grid_height
                    grid_c: int = c + dc
                    grid_c = (
                        grid_c + self.world_specs.grid_width
                    ) % self.world_specs.grid_width
                    neighbor_jellies.extend(
                        self.grid_space_old[grid_r][grid_c].jellyfish.values()
                    )

            afraid_of_fish: list[Fish] = []
            r: int = int(jellyfish.position.y / self.world_specs.cell_size)
            c: int = int(jellyfish.position.x / self.world_specs.cell_size)
            for dr in range(-scared_range, scared_range + 1):
                for dc in range(-scared_range, scared_range + 1):
                    grid_r: int = r + dr
                    grid_r = (
                        grid_r + self.world_specs.grid_height
                    ) % self.world_specs.grid_height
                    grid_c: int = c + dc
                    grid_c = (
                        grid_c + self.world_specs.grid_width
                    ) % self.world_specs.grid_width
                    for fish in self.grid_space_old[grid_r][grid_c].fish.values():
                        if (
                            self.schools[fish.group_id].fish_settings.fish_type
                            == FishType.RED
                        ):
                            afraid_of_fish.append(fish)

            jellyfish.update_acceleration(
                self.player.position,
                neighbor_jellies,
                afraid_of_fish,
                self.world_specs.world_width,
            )

        # Move all the jellyfish: this should only be done after all accelerations have been applied to them for the current frame
        for jellyfish in self.jellyfish.values():
            old_r = int(jellyfish.position.y / self.world_specs.cell_size)
            old_c = int(jellyfish.position.x / self.world_specs.cell_size)
            jellyfish.update_position(
                self.world_specs.world_width,
                self.world_specs.world_height,
                dt,
            )
            # Check if we are in a new grid cell after moving
            new_r = int(jellyfish.position.y / self.world_specs.cell_size)
            new_c = int(jellyfish.position.x / self.world_specs.cell_size)
            if new_r != old_r or new_c != old_c:
                del self.grid_space_old[old_r][old_c].jellyfish[jellyfish.entity_id]
                self.grid_space_old[new_r][new_c].jellyfish[jellyfish.entity_id] = jellyfish
