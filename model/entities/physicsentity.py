from abc import ABC
from uuid import UUID

from pygame import Surface, Vector2

from model.entities.entity import Entity
from model.utils.vectorutils import limit_magnitude, safe_normalize
from model.world.modelcontext import ModelContext


class PhysicsEntity(Entity, ABC):
    """
    Abstract class for entities that move using velocity and acceleration
    """
    def __init__(
            self,
            sprite: Surface,
            manager_id: UUID,
            max_speed: float,
            max_acceleration: float
    ) -> None:
        super().__init__(sprite, manager_id)
        self._velocity: Vector2 = Vector2(0.0, 0.0)
        self._acceleration: Vector2 = Vector2(0.0, 0.0)
        self._max_speed: float = max_speed
        self._max_acceleration: float = max_acceleration

    def move(self, context: ModelContext, dt: float) -> None:
        self._velocity += (self._acceleration * dt)
        limit_magnitude(self._velocity, self._max_speed)
        self._position += self._velocity * dt
        self._position.x = (self._position.x + context.get_world_w()) % context.get_world_w()
        if self._position.y < 0:
            self._position.y = 0
        if self._position.y >= context.get_world_h():
            self._position.y = context.get_world_h() - 1
        # Acceleration is reset each frame
        self._acceleration *= 0.0

    def target(self, target_dir: Vector2, k: float) -> None:
        """
        Accelerates this entity in the target direction.
        """
        safe_normalize(target_dir)
        target_dir *= self._max_speed
        target_dir -= self._velocity
        limit_magnitude(target_dir, self._max_acceleration)
        target_dir *= k
        self._acceleration += target_dir

    def get_velocity(self) -> Vector2:
        return self._velocity

    def set_velocity(self, v: Vector2) -> None:
        self._velocity = v

    def get_acceleration(self) -> Vector2:
        return self._acceleration

    def apply_acceleration(self, a: Vector2) -> None:
        """
        Adds the provided acceleration vector to this entity's acceleration for the current frame.
        """
        self._acceleration += a

    def get_max_speed(self) -> float:
        return self._max_speed

    def get_max_acceleration(self) -> float:
        return self._max_acceleration
