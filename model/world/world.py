import random
from typing import Tuple
from uuid import UUID

import pygame
from pygame import Surface
from pygame.key import ScancodeWrapper

from model.entities.fish.fish import Fish
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

    def initialize_grid_space(self) -> list[list[GridCell]]:
        grid_space: list[list[GridCell]] = []
        for row in range(self.grid_height):
            grid_space.append([])
            for col in range(self.grid_width):
                background: Surface = pygame.Surface((self.cell_size, self.cell_size))
                noise: int = random.randint(0, 25)
                background.fill((0, 50 + noise, 115 + noise * 2))
                grid_space[row].append(GridCell(self.cell_size, row, col, background))
        return grid_space

    def hatch_schools(self):
        for school in self.schools.values():
            for _ in range(school.school_params.egg_count):
                self.spawn_fish_in_grid_space(school.hatch_fish())

    def update_model(self, dt: float, key_presses: ScancodeWrapper) -> None:
        self.update_fish(dt)
        self.spawn_jellyfish(dt)
        self.update_jellyfish(dt)
        self.player.move_player(key_presses, dt)
        # TODO collision detection with player/jellies

    ##############################
    ######## Fish functions ######
    ##############################

    def add_school(self, school: School) -> None:
        self.schools[school.school_id] = school

    def spawn_fish_in_grid_space(self, new_fish: Fish) -> None:
        self.grid_space[int(new_fish.position.y / self.cell_size)][
            int(new_fish.position.x / self.cell_size)
        ].fish.append(new_fish)

    def update_fish(self, dt: float):
        # Have all the fish make schooling decisions based on their current location and velocity
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                for current_fish in self.grid_space[row][col].fish:
                    self.find_neighbors_and_make_schooling_decisions(current_fish)

        # A list of Tuples to help keep track of fish that move grid cells during their position updates
        fish_changed_cells: list[Tuple[int, int, Fish]] = []
        # Move all the fish: this should only be done after all schooling decisions have been made for the current frame
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                for i in range(len(self.grid_space[row][col].fish) - 1, -1, -1):
                    f: Fish = self.grid_space[row][col].fish[i]
                    f.update_position(self.world_width, self.world_height, dt)
                    # Check if we are in a new grid cell after moving
                    new_r = int(f.position.y / self.cell_size)
                    new_c = int(f.position.x / self.cell_size)
                    if new_r != row or new_c != col:
                        # Remove the fish from the current list
                        del self.grid_space[row][col].fish[i]
                        # Track the fish that was just removed in the list of grid cell updates
                        fish_changed_cells.append((new_r, new_c, f))
        # Update grid cells with entities that moved into new cells:
        # This must be done after all entities have moved otherwise we run the risk of processing an entity's position update twice
        for cell_fish in fish_changed_cells:
            self.grid_space[cell_fish[0]][cell_fish[1]].fish.append(cell_fish[2])

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
                neighbors.extend(self.grid_space[grid_r][grid_c].fish)
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
                # Add the jelly to gridspace
                self.grid_space[int(new_jelly.position.y / self.cell_size)][
                    int(new_jelly.position.x / self.cell_size)
                ].jellyfish[new_jelly.uuid] = new_jelly
            # reset jelly spawn timer
            self.jelly_spawner_timer = self.jelly_spawner_delay

    def update_jellyfish(self, dt: float):
        # Apply acceleration to all the jellies
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                for jellyfish in self.grid_space[row][col].jellyfish.values():
                    jellyfish.accelerate_towards_player(self.player.position)

        # Track jellies that change cells when they move
        jellies_changed_cells: list[Tuple[int, int, Jellyfish]] = []
        # Move all the jellyfish: this should only be done after all accelerations have been applied to them for the current frame
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                for key in list(self.grid_space[row][col].jellyfish.keys()):
                    jelly = self.grid_space[row][col].jellyfish[key]
                    jelly.update_position(self.world_width, self.world_height, dt)
                    # Check if we are in a new grid cell after moving
                    new_r = int(jelly.position.y / self.cell_size)
                    new_c = int(jelly.position.x / self.cell_size)
                    if new_r != row or new_c != col:
                        del self.grid_space[row][col].jellyfish[key]
                        jellies_changed_cells.append((new_r, new_c, jelly))

        # Update grid cells with jellyfish that moved into new cells:
        # This must be done after all jellyfish have moved otherwise we run the risk of processing a jellyfish's position update twice
        for cell_jelly in jellies_changed_cells:
            self.grid_space[cell_jelly[0]][cell_jelly[1]].jellyfish[cell_jelly[2].uuid] = cell_jelly[2]

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
                entities.extend(self.grid_space[r][c].fish)
                entities.extend(self.grid_space[r][c].jellyfish.values())
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
