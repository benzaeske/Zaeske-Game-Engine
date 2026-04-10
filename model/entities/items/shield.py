from uuid import UUID

from pygame import Rect
from pygame.math import Vector2

from model.entities.entity import Entity
from model.entities.entitytype import EntityType
from model.entities.items.shieldconfig import ShieldConfig
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from model.world.modelcontext import ModelContext


class Shield(Entity):
    def __init__(self, config: ShieldConfig, manager_id: UUID) -> None:
        super().__init__(config, manager_id)
        self.charge: int = 0
        self._max_charge: int = config.max_charge
        self._charge_timer: float = 0.0
        self._charge_delay: float = config.charge_delay
        self._radius = config.radius
        self._radius_squared: float = self._radius * self._radius
        self._damage: float = config.damage

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        if context.player.get_fish_coherency(EntityType.YELLOW_FISH):
            self._charge_timer += dt
            if self._charge_timer >= self._charge_delay:
                self.increment_charge()
                self._charge_timer = 0.0
        if self.charge > 0:
            self.process_enemy_collisions(context)

    def move(self, context: ModelContext, dt: float) -> None:
        self._position = context.player.get_position()

    def increment_charge(self) -> None:
        self.charge += 1
        if self.charge > self._max_charge:
            self.charge = self._max_charge

    def decrement_charge(self) -> None:
        self.charge -= 1
        if self.charge < 0:
            self.charge = 0

    def process_enemy_collisions(self, context: ModelContext) -> None:
        collided_with_enemies: bool = False
        for enemy in context.grid_space.get_neighbors(self._position, 2,
                                                      context.entity_repository.get_manager_ids(EntityManagerIndex.ENEMY)):
            hitbox: Rect = enemy.get_hitbox()
            # Find the closest point on the enemy's hitbox to the center of the circular shield
            closest_point: Vector2 = Vector2(
                max(hitbox.left, min(int(self.get_x()), hitbox.right)),
                max(hitbox.top, min(int(self.get_y()), hitbox.bottom))
            )
            # Enemy collision if the closest point is within a distance less than the shield's radius
            if self.get_position().distance_squared_to(closest_point) <= self._radius_squared:
                enemy.update_hp(-self._damage)
                collided_with_enemies = True
        # Only decrement shield charge once per frame even if multiple enemies collided
        if collided_with_enemies:
            self.decrement_charge()

    def get_current_charge(self) -> int:
        return self.charge

    def get_max_charge(self) -> int:
        return self._max_charge

    def get_radius(self) -> float:
        return self._radius