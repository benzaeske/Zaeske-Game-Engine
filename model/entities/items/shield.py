from uuid import UUID

from pygame import Rect
from pygame.math import Vector2

from model.entities.entity import Entity
from model.entities.items.shieldconfig import ShieldConfig
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from model.world.modelcontext import ModelContext


class Shield(Entity):
    def __init__(self, config: ShieldConfig, manager_id: UUID) -> None:
        super().__init__(config, manager_id)
        self._radius = config.radius
        self._radius_squared: float = self._radius * self._radius
        self._damage: float = config.damage
        self._knockback_force: float = config.knockback_force
        self._cooldown: float = config.cooldown
        self._hit_cooldowns: dict[UUID, float] = {}

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        self._process_entity_hit_cooldowns(dt)
        self.process_enemy_collisions(context)

    def _process_entity_hit_cooldowns(self, dt) -> None:
        """
        Decrements all hit cooldowns and removes any that are finished
        """
        for entity_id in list(self._hit_cooldowns.keys()):
            self._hit_cooldowns[entity_id] -= dt
            if self._hit_cooldowns[entity_id] <= 0:
                self._hit_cooldowns.pop(entity_id)

    def process_enemy_collisions(self, context: ModelContext) -> None:
        for enemy in context.grid_space.get_neighbors(self._position, 2,
                                                      context.entity_repository.get_manager_ids(EntityManagerIndex.ENEMY)):
            if enemy.get_id() not in self._hit_cooldowns:
                hitbox: Rect = enemy.get_hitbox()
                # Find the closest point on the enemy's hitbox to the center of the circular shield
                closest_point: Vector2 = Vector2(
                    max(hitbox.left, min(int(self.get_x()), hitbox.right)),
                    max(hitbox.top, min(int(self.get_y()), hitbox.bottom))
                )
                # Enemy collision if the closest point is within a distance less than the shield's radius
                if self.get_position().distance_squared_to(closest_point) <= self._radius_squared:
                    enemy.update_hp(-self._damage)
                    enemy.apply_knockback(self._knockback_force)
                    self._hit_cooldowns[enemy.get_id()] = self._cooldown

    def move(self, context: ModelContext, dt: float) -> None:
        self._position = context.player.get_position()

    def get_radius(self) -> float:
        return self._radius