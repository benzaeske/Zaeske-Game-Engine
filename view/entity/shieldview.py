from pygame import Surface, draw, SRCALPHA

from controller.camera import Camera
from model.entities.entitytype import EntityType
from model.entities.items.shield import Shield
from view.entity.entityview import EntityView
from view.sprite.spritecatalog import SpriteCatalog
from view.sprite.spritedata import SpriteData


class ShieldView(EntityView[Shield]):
    def __init__(self, shield: Shield, sprite_catalog: SpriteCatalog) -> None:
        super().__init__(shield, sprite_catalog)
        self._shield_sprite: SpriteData = sprite_catalog.get_entity_sprite_data(EntityType.SHIELD)

    def draw_entity(self, screen: Surface, camera: Camera, dt: float) -> None:
        screen.blit(
            self._shield_sprite.get_surface(),
            self.to_camera_pos(camera.get_window(), self._shield_sprite.get_width_adj(), self._shield_sprite.get_height_adj())
        )