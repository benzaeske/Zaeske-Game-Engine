from pygame import Surface

from controller.camera import Camera
from model.entities.enemies.enemy import Enemy
from view.entity.entityview import EntityView
from view.sprite.spritecatalog import SpriteCatalog
from view.sprite.spritedata import SpriteData


class EnemyView(EntityView[Enemy]):
    def __init__(self, enemy: Enemy, sprite_catalog: SpriteCatalog) -> None:
        super().__init__(enemy, sprite_catalog)
        self._sprite_data: SpriteData = self._get_sprite_data()

    def draw_entity(self, screen: Surface, camera: Camera, dt: float) -> None:
        # Draw the enemy sprite directly on screen at its current location
        screen.blit(
            self._sprite_data.get_surface(),
            self.to_camera_pos(camera.get_window(), self._sprite_data.get_width_adj(), self._sprite_data.get_height_adj())
        )