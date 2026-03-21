import pygame
from pygame import Vector2, Rect
from pygame.key import ScancodeWrapper

from model.entity.fish.fishconfig import FishType
from model.modelutils import limit_magnitude
from model.player.camera import Camera
from model.player.playerinterface import PlayerInterface
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from model.world.entityrepository.entityrepositoryinterface import EntityRepositoryInterface
from model.world.gridspace.grid_cell import GridCell
from model.world.gridspace.gridspaceinterface import GridSpaceInterface

class Player(PlayerInterface):
    def __init__(
        self,
        camera: Camera,
        hitbox_width: float,
        hitbox_height: float,
        max_speed: float,
        max_acceleration: float,
        max_health: float
    ) -> None:
        super().__init__()
        self._camera: Camera = camera # TODO camera in controller not on player
        self._position: Vector2 = Vector2(0.0, 0.0)
        self._velocity: Vector2 = Vector2(0.0, 0.0)
        self._max_speed: float = max_speed
        self._acceleration: Vector2 = Vector2(0.0, 0.0)
        self._max_acceleration: float = max_acceleration
        self._hitbox: Rect = Rect(0, 0, hitbox_width, hitbox_height)
        self._max_health: float = max_health
        self._current_health: float = self._max_health
        self._fish_coherency: dict[FishType, int] = {}
        self._facing_direction: int = 0

    def frame_actions(self, grid_space: GridSpaceInterface, entity_repository: EntityRepositoryInterface, dt: float) -> None:
        self.process_enemy_collisions(grid_space, entity_repository, dt)
        self.process_fish_coherency(grid_space, entity_repository)

    def move(self, key_presses: ScancodeWrapper, dt: float) -> None:
        self._acceleration = Vector2(0.0, 0.0)
        # Calculate acceleration as the sum of key presses
        if key_presses[pygame.K_LEFT]:
            self._acceleration += Vector2(-self._max_speed, 0)
        if key_presses[pygame.K_RIGHT]:
            self._acceleration += Vector2(self._max_speed, 0)
        if key_presses[pygame.K_UP]:
            self._acceleration += Vector2(0, self._max_speed)
        if key_presses[pygame.K_DOWN]:
            self._acceleration += Vector2(0, -self._max_speed)
        limit_magnitude(self._acceleration, self._max_acceleration)
        self._velocity += (self._acceleration * dt)
        if self._acceleration.x == 0:
            self._velocity.x += ((-self._velocity.x / 4) * dt)
        if self._acceleration.y == 0:
            self._velocity.y += ((-self._velocity.y / 4) * dt)
        limit_magnitude(self._velocity, self._max_speed)
        self._position += (self._velocity * dt)
        # Update facing direction for drawing
        if self._velocity.x != 0:
            if self._velocity.x > 0:
                self._facing_direction = 1
            else:
                self._facing_direction = 0
        self._hitbox.center = self._position
        self._camera.set_window_position(self._position)

    def process_enemy_collisions(self, grid_space: GridSpaceInterface, entity_repository: EntityRepositoryInterface,
                                 dt: float) -> None:
        cell_range: int = 1
        for enemy in grid_space.get_neighbors(self._position, cell_range,
                                              entity_repository.get_manager_ids(EntityManagerIndex.ENEMY)):
            if enemy.get_hitbox().colliderect(self._hitbox):
                self.update_health(-enemy.get_damage() * dt)

    def process_fish_coherency(self, grid_space: GridSpaceInterface,
                               entity_repository: EntityRepositoryInterface) -> None:
        p_grid_cell: GridCell = grid_space.get_grid_cell(self._position)
        if p_grid_cell is not None:
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

    def get_position(self) -> Vector2:
        return self._position

    def get_velocity(self) -> Vector2:
        return self._velocity

    def get_acceleration(self) -> Vector2:
        return self._acceleration

    def get_hitbox(self) -> Rect:
        return self._hitbox

    def get_camera(self) -> Camera:
        return self._camera

    def get_current_health(self) -> float:
        return self._current_health

    def get_max_health(self) -> float:
        return self._max_health

    def update_health(self, hp_diff: float) -> None:
        self._current_health += hp_diff
        if self._current_health > self._max_health:
            self._current_health = self._max_health
        if self._current_health < 0:
            self._current_health = 0

    def get_fish_coherency(self, fish_type: FishType) -> int:
        return self._fish_coherency.get(fish_type, 0)