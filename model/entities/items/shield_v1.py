from uuid import UUID

from pygame import Surface, SRCALPHA, draw

from model.entities.entity import Entity
from model.world.modelcontext import ModelContext


class Shield_v1(Entity):
    def __init__(self, manager_id: UUID, shield_radius: float):
        self._shield_radius: float = shield_radius
        self._shield_radius_squared: float = self._shield_radius * self._shield_radius
        super().__init__(self.get_shield_surface(), manager_id)
        self._max_shield: int = 10
        self._shield_charge: int = 0
        self._shield_charge_delay: float = 1.0
        self._shield_charge_cooldown: float = 0.0
        self._shield_alpha_scaling: int = 10
        self._shield_damage: float = 100.0

    def get_shield_surface(self) -> Surface:
        shield_surface: Surface = Surface(
            (self._shield_radius * 2, self._shield_radius * 2), SRCALPHA
        )
        draw.circle(
            shield_surface,
            (
                255,
                255,
                0,
                self._shield_alpha_scaling + (self._shield_charge * self._shield_alpha_scaling),
            ),
            shield_surface.get_rect().center,
            self._shield_radius,
        )
        return shield_surface

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        pass

    def move(self, context: ModelContext, dt: float) -> None:
        pass

    def update_sprite(self):
        self._sprite = self.get_shield_surface()

    def charge_shield(self, dt) -> None:
        if self._shield_charge < self._max_shield:
            self._shield_charge_cooldown += dt
            if self._shield_charge_cooldown >= self._shield_charge_delay:
                self._shield_charge_cooldown = 0.0
                self.increment_shield()

    def increment_shield(self) -> None:
        if self._shield_charge < self._max_shield:
            self._shield_charge += 1

    def decrement_shield(self) -> None:
        if self._shield_charge > 0:
            self._shield_charge -= 1

    def get_shield_charge(self) -> int:
        return self._shield_charge

    def get_shield_radius_squared(self) -> float:
        return self._shield_radius_squared

    def get_shield_damage(self) -> float:
        return self._shield_damage
