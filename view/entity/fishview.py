import math

from pygame import Surface, transform

from model.entities.fish.fish import Fish
from controller.camera import Camera
from view.entity.entityview import EntityView
from view.sprite.spritecatalog import SpriteCatalog
from view.sprite.spritedata import SpriteData


class FishView(EntityView[Fish]):
    def __init__(self, fish: Fish, sprite_catalog: SpriteCatalog) -> None:
        super().__init__(fish, sprite_catalog)
        self._sprite_data: SpriteData = self._get_sprite_data()

    def draw_entity(self, screen: Surface, camera: Camera, dt: float) -> None:
        # Rotate the fish according to its velocity then blit it to the screen.
        screen.blit(
            transform.rotate(
                self._sprite_data.get_surface(),
                math.degrees(math.atan2(self._entity.get_velocity().y, self._entity.get_velocity().x))
            ),
            self.to_camera_pos(camera.get_window(), self._sprite_data.get_width_adj(), self._sprite_data.get_height_adj())
        )