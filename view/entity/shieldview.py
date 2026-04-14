from pygame import Surface, draw, SRCALPHA

from controller.camera import Camera
from model.entities.items.shield import Shield
from view.entity.entityview import EntityView
from view.sprite.spritecatalog import SpriteCatalog


class ShieldView(EntityView[Shield]):
    def __init__(self, shield: Shield, sprite_catalog: SpriteCatalog) -> None:
        super().__init__(shield, sprite_catalog)
        self._shield_sprite: Surface = self._load_shield_sprite()

    def _load_shield_sprite(self) -> Surface:
        shield_sprite: Surface = Surface(
            (self._entity.get_radius() * 2, self._entity.get_radius() * 2),
            SRCALPHA  # This flag allows the surface to have an opacity setting
        )
        draw.circle(
            shield_sprite,
            (255, 255, 0, 64),  # Alpha channel determines opacity
            (self._entity.get_radius(), self._entity.get_radius()),
            self._entity.get_radius()
        )
        shield_sprite.convert_alpha()
        return shield_sprite

    def draw_entity(self, screen: Surface, camera: Camera, dt: float) -> None:
        screen.blit(
            self._shield_sprite,
            self.to_camera_pos(camera.get_window(), self._entity.get_radius(), self._entity.get_radius())
        )