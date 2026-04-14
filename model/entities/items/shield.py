from uuid import UUID

from pygame import Rect
from pygame.math import Vector2

from model.entities.enemies.enemy import Enemy
from model.entities.items.projectile import Projectile
from model.entities.items.shieldconfig import ShieldConfig
from model.world.modelcontext import ModelContext


class Shield(Projectile):
    def __init__(self, config: ShieldConfig, manager_id: UUID) -> None:
        super().__init__(config, manager_id)
        self._radius = config.radius
        self._radius_squared: float = self._radius * self._radius
        self._damage: float = config.damage
        self._knockback_force: float = config.knockback_force
        self._cooldown: float = config.cooldown
        self._hit_cooldowns: dict[UUID, float] = {}

    def collides_with(self, enemy: Enemy) -> bool:
        hitbox: Rect = enemy.get_hitbox()
        # Find the closest point on the enemy's hitbox to the center of the circular shield
        closest_point: Vector2 = Vector2(
            max(hitbox.left, min(int(self.get_x()), hitbox.right)),
            max(hitbox.top, min(int(self.get_y()), hitbox.bottom))
        )
        # Enemy collision if the closest point is within a distance less than the shield's radius
        return self.get_position().distance_squared_to(closest_point) <= self._radius_squared

    def move(self, context: ModelContext, dt: float) -> None:
        self._position = context.player.get_position()

    def get_radius(self) -> float:
        return self._radius