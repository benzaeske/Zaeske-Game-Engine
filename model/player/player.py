from abc import ABC, abstractmethod

import pygame
from pygame import Surface, Vector2, Rect
from pygame.key import ScancodeWrapper

from model.entities.fishconfig import FishType
from model.player.camera import Camera
from model.player.playerinterface import PlayerInterface
from model.utils.vectorutils import limit_magnitude
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from model.world.entityrepository.entityrepositoryinterface import EntityRepositoryInterface
from model.world.gridspace.grid_cell import GridCell
from model.world.gridspace.gridspaceinterface import GridSpaceInterface

class Player(PlayerInterface, ABC):
    def __init__(
        self,
        camera_width: float,
        camera_height: float,
        hitbox_width: float,
        hitbox_height: float,
        max_speed: float,
        max_health: float
    ) -> None:
        super().__init__()
        self._position: Vector2 = Vector2(0.0, 0.0)
        self._hitbox: Rect = Rect(0, 0, hitbox_width, hitbox_height)
        self._camera: Camera = Camera(camera_width, camera_height)
        self._max_speed: float = max_speed
        self._max_health: float = max_health
        self._current_health: float = self._max_health
        self._fish_coherency: dict[FishType, int] = {}
        self._facing_direction: int = 0

    def update(self, grid_space: GridSpaceInterface, entity_repository: EntityRepositoryInterface, dt: float) -> None:
        self.process_enemy_collisions(grid_space, entity_repository, dt)
        self.process_fish_coherency(grid_space, entity_repository)

    def process_enemy_collisions(self, grid_space: GridSpaceInterface, entity_repository: EntityRepositoryInterface,
                                 dt: float) -> None:
        cell_range: int = 1
        for enemy in grid_space.get_neighbors(self._position, cell_range,
                                              entity_repository.get_manager_ids(EntityManagerIndex.ENEMY)):
            if enemy.get_hitbox().colliderect(self._hitbox):
                self.update_hp(-enemy.get_damage() * dt)

    def process_fish_coherency(self, grid_space: GridSpaceInterface,
                               entity_repository: EntityRepositoryInterface) -> None:
        p_grid_cell: GridCell = grid_space.get_grid_cell(self._position)
        self._fish_coherency[FishType.RED] = len(
            p_grid_cell.get_entities_by_manager_ids(
                entity_repository.get_manager_ids(EntityManagerIndex.RED_FISH)
            )
        )
        self._fish_coherency[FishType.YELLOW] = len(
            p_grid_cell.get_entities_by_manager_ids(
                entity_repository.get_manager_ids(EntityManagerIndex.YELLOW_FISH)
            )
        )
        self._fish_coherency[FishType.GREEN] = len(
            p_grid_cell.get_entities_by_manager_ids(
                entity_repository.get_manager_ids(EntityManagerIndex.GREEN_FISH)
            )
        )

    def move_player(self, key_presses: ScancodeWrapper, dt: float) -> None:
        """
        Moves the player according to the keys pressed. Movement is scaled with delta time like all other entities.
        Limits the camera position to be confined within positive x,y coordinates and under the provided world boundary.
        """
        velocity: Vector2 = Vector2(0.0, 0.0)
        # Calculate velocity as the sum of key presses
        if key_presses[pygame.K_LEFT]:
            velocity += Vector2(-self._max_speed, 0)
        if key_presses[pygame.K_RIGHT]:
            velocity += Vector2(self._max_speed, 0)
        if key_presses[pygame.K_UP]:
            velocity += Vector2(0, self._max_speed)
        if key_presses[pygame.K_DOWN]:
            velocity += Vector2(0, -self._max_speed)
        limit_magnitude(velocity, self._max_speed)
        self._position += velocity * dt
        self._hitbox.center = self._position
        self._camera.set_window_position(self._position)
        # Update facing direction for drawing
        if velocity.x != 0:
            if velocity.x > 0:
                self._facing_direction = 1
            else:
                self._facing_direction = 0

    def get_position(self) -> Vector2:
        return self._position

    def get_camera(self) -> Camera:
        return self._camera

    def update_hp(self, hp_diff: float) -> None:
        self._current_health += hp_diff
        if self._current_health > self._max_health:
            self._current_health = self._max_health
        if self._current_health < 0:
            self._current_health = 0

    def get_fish_coherency(self, fish_type: FishType) -> int:
        return self._fish_coherency.get(fish_type, 0)

    @abstractmethod
    def draw(self, screen: Surface) -> None:
        pass