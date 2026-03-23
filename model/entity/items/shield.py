import copy
from uuid import UUID

from pygame import Rect
from pygame.math import Vector2

from model.entity.entity import Entity
from model.entity.fish.fishconfig import FishType
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from model.world.modelcontext import ModelContext


class Shield(Entity):
    def __init__(self, manager_id: UUID, shield_radius: float, shield_damage: float) -> None:
        super().__init__(manager_id)
        self._shield_charge: int = 5
        self._max_shield_charge: int = 10
        self._shield_charge_timer: float = 0.0
        self._shield_charge_delay: float = 0.5
        self._shield_radius = shield_radius
        self._shield_radius_squared: float = self._shield_radius * self._shield_radius
        self._shield_damage: float = shield_damage

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        if context.player.get_fish_coherency(FishType.YELLOW):
            self._shield_charge_timer += dt
            if self._shield_charge_timer >= self._shield_charge_delay:
                self.increment_shield_charge()
                self._shield_charge_timer = 0.0
        if self._shield_charge > 0:
            self.process_enemy_collisions(context)

    def move(self, context: ModelContext, dt: float) -> None:
        self._position = context.player.get_position()

    def increment_shield_charge(self) -> None:
        self._shield_charge += 1
        if self._shield_charge > self._max_shield_charge:
            self._shield_charge = self._max_shield_charge

    def decrement_shield_charge(self) -> None:
        self._shield_charge -= 1
        if self._shield_charge < 0:
            self._shield_charge = 0

    def process_enemy_collisions(self, context: ModelContext) -> None:
        collided_with_enemies: bool = False
        for enemy in context.grid_space.get_neighbors(self._position, 1,
                                                      context.entity_repository.get_manager_ids(EntityManagerIndex.ENEMY)):
            hitbox: Rect = enemy.get_hitbox()
            # Find the closest point on the enemy's hitbox to the center of the circular shield
            closest_point: Vector2 = Vector2(
                max(hitbox.left, min(int(self.get_x()), hitbox.right)),
                max(hitbox.top, min(int(self.get_y()), hitbox.bottom))
            )
            # Enemy collision if the closest point is within a distance less than the shield's radius
            if self.get_position().distance_squared_to(closest_point) <= self._shield_radius_squared:
                enemy.update_hp(-self._shield_damage)
                collided_with_enemies = True
        if collided_with_enemies:
            pass
            #self.decrement_shield_charge()

    def get_current_shield_charge(self) -> int:
        return self._shield_charge

    def get_max_shield_charge(self) -> int:
        return self._max_shield_charge

    def get_shield_radius(self) -> float:
        return self._shield_radius

