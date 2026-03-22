from pygame import Surface

from model.entity.enemies.jellyfish import Jellyfish
from controller.camera import Camera
from view.entity.entityview import EntityView
from view.sprite.entityanimation import EntityAnimation
from view.sprite.spritecatalog import SpriteCatalog
from view.sprite.spritesheet import SpriteSheet


class JellyfishView(EntityView[Jellyfish]):
    def __init__(self, jellyfish: Jellyfish, sprite_catalog: SpriteCatalog) -> None:
        super().__init__(jellyfish, sprite_catalog)
        self._sprite_sheet: SpriteSheet = sprite_catalog.get_entity_animation(EntityAnimation.RED_JELLYFISH)
        self._current_animation_frame: int = 0
        self._animation_timer: float = 0.0

    def draw_entity(self, screen: Surface, camera: Camera, dt: float) -> None:
        # Basic implementation that switches between surfaces in the sprite sheet based on how long the current surface
        # has been shown. This may become a base class for entity views later
        self._animation_timer += dt
        if self._animation_timer >= self._sprite_sheet.get_frame_duration(self._current_animation_frame):
            self._current_animation_frame += 1
            self._current_animation_frame %= self._sprite_sheet.get_num_frames()
        screen.blit(
            self._sprite_sheet.get_sprite(self._current_animation_frame),
            self.to_camera_pos(
                camera.get_window(),
                self._sprite_sheet.get_width_adj(),
                self._sprite_sheet.get_height_adj()
            )
        )