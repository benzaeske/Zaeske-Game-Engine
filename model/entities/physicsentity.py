from abc import ABC
from copy import copy
from typing import Optional
from uuid import UUID

from pygame import Vector2

from model.entities.entity import Entity
from model.entities.knockback import Knockback
from model.entities.physicsentityconfig import PhysicsEntityConfig
from model.modelutils import limit_magnitude, safe_normalize
from model.world.modelcontext import ModelContext


class PhysicsEntity(Entity, ABC):
    """
    Abstract class for entity that move using velocity and acceleration
    """
    def __init__(self, config: PhysicsEntityConfig, manager_id: UUID) -> None:
        super().__init__(config, manager_id)
        self._velocity: Vector2 = Vector2(0.0, 0.0)
        self._acceleration: Vector2 = Vector2(0.0, 0.0)
        self._max_speed: float = config.max_speed
        self._max_acceleration: float = config.max_acceleration
        self._knockback: list[Knockback] = []

    def move(self, context: ModelContext, dt: float) -> None:
        self._velocity += (self._acceleration * dt)
        limit_magnitude(self._velocity, self._max_speed)
        # Self-imposed acceleration is reset each frame
        self._acceleration *= 0.0
        if len(self._knockback) == 0:
            self._position += self._velocity * dt
        else:
            self._process_knockback(context, dt)

    def _process_knockback(self, context: ModelContext, dt: float) -> None:
        """
        Moves this entity according to knockback. Assumes that _knockback list is not empty. Any component of the
        entity's velocity that is moving towards the player will be reversed. The altered velocity is then multiplied
        by the total sum of all knockback forces currently applied to this entity without regard to max speed.
        """
        total_k: float = 0.0
        for i in range(len(self._knockback) -1, -1, -1):
            knockback: Knockback = self._knockback[i]
            total_k += knockback.get_magnitude()
            knockback.decrement_timer(dt)
            if knockback.get_remaining_duration() <= 0.0:
                self._knockback.pop(i)
        # Reverse any component of the current velocity that is heading towards the player
        diff: Vector2 = self.get_position() - context.player.get_position() # A vector pointing from the player to the entity
        alter_x: float = 1.0 if (diff.x <= 0) == (self.get_velocity().x <= 0) else -1.0 # Reverse if sign is different
        alter_y: float = 1.0 if (diff.y <= 0) == (self.get_velocity().y <= 0) else -1.0 # Reverse if sign is different
        knockback_v: Vector2 = Vector2(alter_x * self.get_velocity().x, alter_y * self.get_velocity().y)
        # Multiply by total knockback constant
        knockback_v *= total_k
        self._position += (knockback_v * dt)

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
        """
        Read only. Returns a shallow copy of this entity's current velocity.
        """
        return copy(self._velocity)

    def set_velocity(self, v: Vector2) -> None:
        self._velocity = v

    def get_acceleration(self) -> Vector2:
        """
        Read only. Returns a shallow copy of this entity's current acceleration.
        """
        return copy(self._acceleration)

    def apply_acceleration(self, a: Vector2) -> None:
        """
        Adds the provided acceleration vector to this entity's acceleration for the current frame.
        """
        self._acceleration += a

    def get_max_speed(self) -> float:
        return self._max_speed

    def get_max_acceleration(self) -> float:
        return self._max_acceleration

    def apply_knockback(self, k: float) -> None:
        self._knockback.append(Knockback(k))