import random
from typing import Tuple
from uuid import UUID

import pygame
from pygame import Surface, Vector2
from pygame.key import ScancodeWrapper

from model.entities.fish.fish import Fish
from model.entities.fish.fishsettings import FishType
from model.entities.gameentity import GameEntity
from model.entities.jellyfish.jellyfish import Jellyfish
from model.entities.jellyfish.jellyfishspawner import JellyfishSpawner
from model.entities.school.school import School
from model.player.player import Player
from model.world.grid_cell import GridCell


class SpatialPartitioningModel:
    """
    Implementation of spatial partitioning. The 'world' is divided into a grid of cells. The size of a cell determines how far entities in the simulation can 'see'.\n
    When applying the schooling algorithm to fish, calculations are only performed on neighbors within the fish's cell and the cells surrounding it as defined by a variable cell detection radius.\n
    For V1, The world width and height must be evenly divisible by cell_size, or array out of bounds issues will occur\n
    """

    def __init__(
        self,
        world_width: float,
        world_height: float,
        cell_size: float,
        player: Player,
    ):
        self.world_width: float = world_width
        self.world_height: float = world_height
        self.cell_size: float = cell_size
        self.grid_width: int = int(self.world_width / self.cell_size)
        self.grid_height: int = int(self.world_height / self.cell_size)
        self.player: Player = player
        self.schools: dict[UUID, School] = {}
        self.jellyfish_spawner: JellyfishSpawner | None = None
        self.jelly_spawner_delay: float = 10.0
        self.jelly_spawner_timer: float = 0.0
        self.grid_space: list[list[GridCell]] = self.initialize_grid_space()

        # rework
        self.fish: dict[UUID, Fish] = {}
        self.jellyfish: dict[UUID, Jellyfish] = {}

    def initialize_grid_space(self) -> list[list[GridCell]]:
        grid_space: list[list[GridCell]] = []
        for row in range(self.grid_height):
            grid_space.append([])
            for col in range(self.grid_width):
                background: Surface = pygame.Surface((self.cell_size, self.cell_size))
                noise: int = random.randint(0, 25)
                if col == 0:
                    background.fill((0, 0, 0))
                elif row == 0:
                    background.fill((99, 85, 52))
                else:
                    background.fill((0, 50 + noise, 115 + noise * 2))
                grid_space[row].append(GridCell(self.cell_size, row, col, background))
        return grid_space

    def hatch_schools(self):
        for school in self.schools.values():
            for _ in range(school.school_params.egg_count):
                self.spawn_fish_in_grid_space(school.hatch_fish())

    def update_model(self, dt: float, key_presses: ScancodeWrapper) -> None:
        self.update_player(dt)
        self.update_fish(dt)
        self.spawn_jellyfish(dt)
        self.update_jellyfish(dt)
        self.player.move_player(key_presses, dt)

    def update_player(self, dt: float) -> None:
        self.process_player_fish_coherency(dt)
        self.process_player_jelly_collisions(dt)

    def process_player_fish_coherency(self, dt: float) -> None:
        r: int = int(self.player.position.y / self.cell_size)
        c: int = int(self.player.position.x / self.cell_size)
        cohere_red: int = 0
        cohere_green: int = 0
        cohere_yellow: int = 0
        for fish in self.grid_space[r][c].fish.values():
            match self.schools.get(fish.school_id).fish_settings.fish_type:
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

    def process_player_jelly_collisions(self, dt: float) -> None:
        cell_range: int = 1
        # Only process collisions for jellies that are within a cell range that can actually reach the player
        r: int = int(self.player.position.y / self.cell_size)
        c: int = int(self.player.position.x / self.cell_size)
        for dr in range(-cell_range, cell_range + 1):
            for dc in range(-cell_range, cell_range + 1):
                grid_r: int = r + dr
                grid_r = (grid_r + self.grid_height) % self.grid_height
                grid_c: int = c + dc
                grid_c = (grid_c + self.grid_width) % self.grid_width
                for jelly in self.grid_space[grid_r][grid_c].jellyfish.values():
                    if jelly.hitbox.colliderect(self.player.hitbox):
                        self.player.health -= (jelly.damage * dt)

    ##############################
    ######## Fish functions ######
    ##############################

    def add_school(self, school: School) -> None:
        self.schools[school.school_id] = school

    def spawn_fish_in_grid_space(self, new_fish: Fish) -> None:
        self.fish[new_fish.uuid] = new_fish
        self.grid_space[int(new_fish.position.y / self.cell_size)][
            int(new_fish.position.x / self.cell_size)
        ].fish[new_fish.uuid] = new_fish

    def update_fish(self, dt: float):
        # Have all the fish make schooling decisions based on their current location and velocity
        for current_fish in self.fish.values():
            self.find_neighbors_and_make_schooling_decisions(current_fish)
        # Move all the fish: this should only be done after all schooling decisions have been made for the current frame
        for current_fish in self.fish.values():
            old_r = int(current_fish.position.y / self.cell_size)
            old_c = int(current_fish.position.x / self.cell_size)
            current_fish.update_position(self.world_width, self.world_height, dt)
            # Check if we are in a new grid cell after moving
            new_r = int(current_fish.position.y / self.cell_size)
            new_c = int(current_fish.position.x / self.cell_size)
            if new_r != old_r or new_c != old_c:
                del self.grid_space[old_r][old_c].fish[current_fish.uuid]
                self.grid_space[new_r][new_c].fish[current_fish.uuid] = current_fish

    def find_neighbors_and_make_schooling_decisions(self, current_fish: Fish) -> None:
        """
        Finds this entity's relevant neighbors and applies the schooling algorithm using only the list of relevant neighbors
        """
        school: School = self.schools[current_fish.school_id]
        cell_range: int = school.school_params.interaction_cell_range
        neighbors: list[Fish] = []
        r: int = int(current_fish.position.y / self.cell_size)
        c: int = int(current_fish.position.x / self.cell_size)
        for dr in range(-cell_range, cell_range + 1):
            for dc in range(-cell_range, cell_range + 1):
                grid_r: int = r + dr
                grid_r = (grid_r + self.grid_height) % self.grid_height
                grid_c: int = c + dc
                grid_c = (grid_c + self.grid_width) % self.grid_width
                neighbors.extend(self.grid_space[grid_r][grid_c].fish.values())
        current_fish.make_schooling_decisions(neighbors, school.school_params)

    ##############################
    ##### Jellyfish functions ####
    ##############################

    def set_jellyfish_spawner(self, spawner: JellyfishSpawner) -> None:
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
                    self.world_width,
                    self.world_height
                )
                self.jellyfish[new_jelly.uuid] = new_jelly
                self.grid_space[int(new_jelly.position.y / self.cell_size)][
                    int(new_jelly.position.x / self.cell_size)
                ].jellyfish[new_jelly.uuid] = new_jelly
            # reset jelly spawn timer
            self.jelly_spawner_timer = self.jelly_spawner_delay
            self.jellyfish_spawner.amount += 1

    def update_jellyfish(self, dt: float):
        if self.player.shield > 0:
            shield_cell_range: int = 2
            # Only process shield collisions for jellies that are within a cell range that can actually reach the player shield
            r: int = int(self.player.position.y / self.cell_size)
            c: int = int(self.player.position.x / self.cell_size)
            for dr in range(-shield_cell_range, shield_cell_range + 1):
                for dc in range(-shield_cell_range, shield_cell_range + 1):
                    grid_r: int = r + dr
                    grid_r = (grid_r + self.grid_height) % self.grid_height
                    grid_c: int = c + dc
                    grid_c = (grid_c + self.grid_width) % self.grid_width
                    for jelly_id in list(self.grid_space[grid_r][grid_c].jellyfish.keys()):
                        jelly = self.grid_space[grid_r][grid_c].jellyfish[jelly_id]
                        # find the closest point on the jelly's hitbox to the player's circular shield
                        closest_point: Vector2 = Vector2(
                            max(jelly.hitbox.left, min(int(self.player.position.x), jelly.hitbox.right)),
                            max(jelly.hitbox.top, min(int(self.player.position.y), jelly.hitbox.bottom))
                        )
                        if closest_point.distance_squared_to(self.player.position) < self.player.shield_radius_squared:
                            self.player.decrement_shield()
                            del self.jellyfish[jelly_id]
                            del self.grid_space[grid_r][grid_c].jellyfish[jelly_id]

        # Avoid jelly neighbors
        neighbor_range: int = 1
        scared_range: int = 3
        for jellyfish in self.jellyfish.values():
            neighbor_jellies: list[Jellyfish] = []
            r: int = int(jellyfish.position.y / self.cell_size)
            c: int = int(jellyfish.position.x / self.cell_size)
            for dr in range(-neighbor_range, neighbor_range + 1):
                for dc in range(-neighbor_range, neighbor_range + 1):
                    grid_r: int = r + dr
                    grid_r = (grid_r + self.grid_height) % self.grid_height
                    grid_c: int = c + dc
                    grid_c = (grid_c + self.grid_width) % self.grid_width
                    neighbor_jellies.extend(self.grid_space[grid_r][grid_c].jellyfish.values())

            afraid_of_fish: list[Fish] = []
            r: int = int(jellyfish.position.y / self.cell_size)
            c: int = int(jellyfish.position.x / self.cell_size)
            for dr in range(-scared_range, scared_range + 1):
                for dc in range(-scared_range, scared_range + 1):
                    grid_r: int = r + dr
                    grid_r = (grid_r + self.grid_height) % self.grid_height
                    grid_c: int = c + dc
                    grid_c = (grid_c + self.grid_width) % self.grid_width
                    for fish in self.grid_space[grid_r][grid_c].fish.values():
                        if self.schools[fish.school_id].fish_settings.fish_type == FishType.RED:
                            afraid_of_fish.append(fish)
            jellyfish.update_acceleration(self.player.position, neighbor_jellies, afraid_of_fish)

        # Move all the jellyfish: this should only be done after all accelerations have been applied to them for the current frame
        for jellyfish in self.jellyfish.values():
            old_r = int(jellyfish.position.y / self.cell_size)
            old_c = int(jellyfish.position.x / self.cell_size)
            jellyfish.update_position(self.world_width, self.world_height, dt)
            # Check if we are in a new grid cell after moving
            new_r = int(jellyfish.position.y / self.cell_size)
            new_c = int(jellyfish.position.x / self.cell_size)
            if new_r != old_r or new_c != old_c:
                del self.grid_space[old_r][old_c].jellyfish[jellyfish.uuid]
                self.grid_space[new_r][new_c].jellyfish[jellyfish.uuid] = jellyfish

    ########################
    ### Helper Functions ###
    ########################

    def get_grid_cells_in_range(
        self, x_range: Tuple[float, float], y_range: Tuple[float, float]
    ) -> list[GridCell]:
        left: int = int(x_range[0] / self.cell_size)
        right: int = int(x_range[1] / self.cell_size)
        bottom: int = int(y_range[0] / self.cell_size)
        top: int = int(y_range[1] / self.cell_size)
        cells: list[GridCell] = []
        for r in range(bottom, top + 1):
            for c in range(left, right + 1):
                cells.append(self.grid_space[r][c])
        return cells

    def get_grid_cells_in_camera_range(self) -> list[GridCell]:
        return self.get_grid_cells_in_range(
            (
                self.player.position.x - self.player.camera_w_adjust,
                self.player.position.x + self.player.camera_w_adjust,
            ),
            (
                self.player.position.y - self.player.camera_h_adjust,
                self.player.position.y + self.player.camera_h_adjust,
            ),
        )

    def get_entities_in_range(
        self, x_range: Tuple[float, float], y_range: Tuple[float, float]
    ) -> list[GameEntity]:
        """
        Finds the grid cells that are within the x, y range specified and returns all entities in those grid cells
        """
        left: int = int(x_range[0] / self.cell_size)
        right: int = int(x_range[1] / self.cell_size)
        bottom: int = int(y_range[0] / self.cell_size)
        top: int = int(y_range[1] / self.cell_size)
        entities: list[GameEntity] = []
        for r in range(bottom, top + 1):
            for c in range(left, right + 1):
                entities.extend(self.grid_space[r][c].fish_old_impl)
                entities.extend(self.grid_space[r][c].jellyfish_old_impl.values())
        return entities

    def get_entities_in_camera_range(self):
        return self.get_entities_in_range(
            (
                self.player.position.x - self.player.camera_w_adjust,
                self.player.position.x + self.player.camera_w_adjust,
            ),
            (
                self.player.position.y - self.player.camera_h_adjust,
                self.player.position.y + self.player.camera_h_adjust,
            ),
        )
