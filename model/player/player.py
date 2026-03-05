import copy
from abc import ABC, abstractmethod
from typing import Tuple
from uuid import UUID

import pygame
from pygame import Surface, Vector2, Rect
from pygame.key import ScancodeWrapper

from model.player.cameraspecs import CameraSpecs
from model.utils.entityutils import calculate_shortest_distance_and_virtual_position
from model.utils.vectorutils import limit_magnitude
from model.world.entitymanagerindex import EntityManagerIndex
from model.world.grid_cell import GridCell
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class Player(ABC):
    def __init__(
        self,
        hitbox_width: float,
        hitbox_height: float,
        surface_width: float,
        surface_height: float,
        camera_specs: CameraSpecs,
        world_specs: WorldSpecs,
        start_pos: Vector2 = Vector2(0.0, 0.0),
        max_speed: float = 1.0,
    ) -> None:
        self.position: Vector2 = start_pos
        self.hitbox: Rect = Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = (int(self.position.x), int(self.position.y))
        self.camera_specs: CameraSpecs = camera_specs
        self.camera: Rect = Rect(
            0, 0, self.camera_specs.camera_width, self.camera_specs.camera_height
        )
        self.camera.center = (int(self.position.x), int(self.position.y))
        self.world_specs: WorldSpecs = world_specs
        self.facing_direction: int = 1
        self.max_speed: float = max_speed
        # Sprite
        self.surface_rect: Rect = Rect(0, 0, surface_width, surface_height)
        self.surface_rect.center = (int(self.position.x), int(self.position.y))
        self.surface_w_adj: float = surface_width / 2
        self.surface_h_adj: float = surface_height / 2
        # Health
        self.max_health: float = 100.0
        self.health: float = self.max_health
        self.max_hp_surface: Surface = pygame.Surface((self.hitbox.width, 10.0))
        self.max_hp_surface.fill((0, 0, 0))
        self.current_hp_surface: Surface = pygame.Surface((self.hitbox.width, 10.0))
        self.current_hp_surface.fill((222, 0, 0))
        # Fish coherency
        self.cohere_red: int = 0
        self.cohere_yellow: int = 0
        self.cohere_green: int = 0

    def update(self, grid_space: GridSpace, entity_manager_indexes: dict[EntityManagerIndex, set[UUID]], dt: float) -> None:
        self.process_fish_coherency(grid_space, entity_manager_indexes)
        self.process_enemy_collisions(grid_space, entity_manager_indexes, dt)

    def process_fish_coherency(self, grid_space: GridSpace, entity_manager_indexes: dict[EntityManagerIndex, set[UUID]]) -> None:
        # Player's grid space coordinate
        p_coord: Tuple[int, int] = grid_space.get_grid_cell_coord_from_position(self.position.x, self.position.y)
        # Player's grid cell
        p_grid_cell: GridCell = grid_space.get_grid_cell(p_coord)
        # Set coherence amounts on player so other functions can reference it quickly
        self.cohere_red = len(
            p_grid_cell.get_entities_by_group_ids(
                entity_manager_indexes.get(EntityManagerIndex.RED_FISH, set())
            )
        )
        self.cohere_yellow = len(
            p_grid_cell.get_entities_by_group_ids(
                entity_manager_indexes.get(EntityManagerIndex.YELLOW_FISH, set())
            )
        )
        self.cohere_green = len(
            p_grid_cell.get_entities_by_group_ids(
                entity_manager_indexes.get(EntityManagerIndex.GREEN_FISH, set())
            )
        )

    def process_enemy_collisions(self, grid_space: GridSpace, entity_manager_indexes: dict[EntityManagerIndex, set[UUID]], dt: float) -> None:
        cell_range: int = 1
        for enemy in grid_space.get_neighbors(self.position.x, self.position.y, cell_range,
                                              entity_manager_indexes.get(EntityManagerIndex.ENEMY, set())):
            enemy_hitbox: Rect = copy.deepcopy(enemy.get_hitbox())
            d, other_pos = calculate_shortest_distance_and_virtual_position(
                self.position, enemy.get_position(), self.world_specs.world_width
            )
            enemy_hitbox.center = other_pos
            if enemy_hitbox.colliderect(self.hitbox):
                self.health -= (enemy.get_damage() * dt)

    def move_player(
        self,
        key_presses: ScancodeWrapper,
        dt: float,
    ) -> None:
        """
        Moves the player according to the keys pressed. Movement is scaled with delta time like all other entities.
        Limits the camera position to be confined within positive x,y coordinates and under the provided world boundary.
        """
        velocity: Vector2 = Vector2(0.0, 0.0)
        # Calculate velocity as the sum of key presses
        if key_presses[pygame.K_LEFT]:
            velocity += Vector2(-self.max_speed, 0)
        if key_presses[pygame.K_RIGHT]:
            velocity += Vector2(self.max_speed, 0)
        if key_presses[pygame.K_UP]:
            velocity += Vector2(0, self.max_speed)
        if key_presses[pygame.K_DOWN]:
            velocity += Vector2(0, -self.max_speed)
        limit_magnitude(velocity, self.max_speed)
        self.position += velocity * dt
        # Wrap on x axis
        self.position.x = (
            self.position.x + self.world_specs.world_width
        ) % self.world_specs.world_width
        # Prevent sprite from leaving world boundary on y-axis
        if self.position.y < self.surface_h_adj:
            self.position.y = self.surface_h_adj
        if self.position.y + self.surface_h_adj >= self.world_specs.world_height:
            self.position.y = self.world_specs.world_height - self.surface_h_adj
        # Update Hitbox
        self.hitbox.center = (int(self.position.x), int(self.position.y))
        # Update sprite
        self.surface_rect.center = (int(self.position.x), int(self.position.y))
        # Update camera. Prevent camera from leaving world boundary on y-axis
        self.camera.center = (int(self.position.x), int(self.position.y))
        if self.camera.bottom >= self.world_specs.world_height - 1:
            self.camera.bottom = int(self.world_specs.world_height) - 1
        if self.camera.top < 0:
            self.camera.top = 0
        # Update facing direction for drawing
        if velocity.x != 0:
            if velocity.x > 0:
                self.facing_direction = 1
            else:
                self.facing_direction = -1

    def draw(self, screen: Surface) -> None:
        pass

    def get_camera_adjusted_position(self) -> Tuple[float, float]:
        return (
            self.surface_rect.left - self.camera.left,
            self.camera.bottom - self.surface_rect.bottom,
        )

    def get_camera_adjusted_hp_pos(self) -> Tuple[float, float]:
        return (
            self.hitbox.left - self.camera.left,
            self.camera.bottom - self.hitbox.top - self.max_hp_surface.get_height(),
        )

    @abstractmethod
    def get_surface(self):
        pass

    def get_cohere_red(self):
        return self.cohere_red

    def get_cohere_green(self):
        return self.cohere_green

    def get_cohere_yellow(self):
        return self.cohere_yellow

class Turtle(Player):
    def __init__(
        self,
        camera_specs: CameraSpecs,
        world_specs: WorldSpecs,
    ) -> None:
        hitbox_width: float = 100.0
        hitbox_height: float = 100.0
        surface_width: float = 128.0
        surface_height: float = 128.0
        turtle_speed: float = 256.0
        self.surface_left: Surface = pygame.image.load("images/baby_turtle_left.png")
        self.surface_left = self.surface_left.convert_alpha()
        self.surface_left = pygame.transform.scale(
            self.surface_left, (surface_width, surface_height)
        )
        self.surface_right: Surface = pygame.image.load("images/baby_turtle_right.png")
        self.surface_right = self.surface_right.convert_alpha()
        self.surface_right = pygame.transform.scale(
            self.surface_right, (surface_width, surface_height)
        )
        super().__init__(
            hitbox_width,
            hitbox_height,
            surface_width,
            surface_height,
            camera_specs,
            world_specs,
            Vector2(world_specs.world_width / 2, world_specs.world_height / 2),
            turtle_speed,
        )

    def get_surface(self):
        if self.facing_direction > 0:
            return self.surface_right
        else:
            return self.surface_left