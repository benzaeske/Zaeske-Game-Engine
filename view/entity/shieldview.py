from pygame import Surface, draw, SRCALPHA

from controller.camera import Camera
from model.entities.items.shield import Shield
from view.entity.entityview import EntityView
from view.sprite.spritecatalog import SpriteCatalog


class ShieldView(EntityView[Shield]):
    def __init__(self, shield: Shield, sprite_catalog: SpriteCatalog) -> None:
        super().__init__(shield, sprite_catalog)
        self._shield_sprites: dict[int, Surface] = self._load_shield_sprites()

    def _load_shield_sprites(self) -> dict[int, Surface]:
        shield_sprites: dict[int, Surface] = {}
        for charge_level in range(1, self._entity.get_max_shield_charge() + 1):
            shield_sprite: Surface = Surface(
                (self._entity.get_shield_radius() * 2, self._entity.get_shield_radius() * 2),
                SRCALPHA # This flag allows the surface to have an opacity setting
            )
            draw.circle(
                shield_sprite,
                (255, 255, 0, 27 + (charge_level * 5)), # Alpha channel determines opacity
                (self._entity.get_shield_radius(), self._entity.get_shield_radius()),
                self._entity.get_shield_radius()
            )
            shield_sprite.convert_alpha()
            shield_sprites[charge_level] = shield_sprite
        return shield_sprites

    def draw_entity(self, screen: Surface, camera: Camera, dt: float) -> None:
        if self._entity.get_current_shield_charge() > 0:
            screen.blit(
                self._shield_sprites.get(self._entity.get_current_shield_charge()),
                self.to_camera_pos(camera.get_window(), self._entity.get_shield_radius(), self._entity.get_shield_radius())
            )