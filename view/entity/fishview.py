import math

from pygame import Surface, transform

from model.entity.fish.fish import Fish
from model.entity.fish.fishconfig import FishType
from model.player.camera import Camera
from view.entity.entityview import EntityView
from view.sprite.entityanimation import EntityAnimation
from view.sprite.spritecatalog import SpriteCatalog
from view.sprite.spritesheet import SpriteSheet


class FishView(EntityView[Fish]):
    def __init__(self, fish: Fish, sprite_catalog: SpriteCatalog) -> None:
        super().__init__(fish, sprite_catalog)
        self._sprite_sheet: SpriteSheet = self.get_sprite_sheet()

    def draw_entity(self, screen: Surface, camera: Camera, dt: float) -> None:
        # Rotate the fish according to its velocity then blit it to the screen.
        screen.blit(
            transform.rotate(
                self._sprite_sheet.get_sprite(0), # Not planning on having fish animation frames any time soon
                math.degrees(math.atan2(self._entity.get_velocity().y, self._entity.get_velocity().x))
            ),
            self.to_camera_pos(camera.get_window(), self._sprite_sheet.get_width_adj(), self._sprite_sheet.get_height_adj())
        )

    def get_sprite_sheet(self) -> SpriteSheet:
        match self._entity.get_fish_type():
            case FishType.RED:
                return self._sprite_catalog.get_entity_animation(EntityAnimation.RED_FISH)
            case FishType.YELLOW:
                return self._sprite_catalog.get_entity_animation(EntityAnimation.YELLOW_FISH)
            case FishType.GREEN:
                return self._sprite_catalog.get_entity_animation(EntityAnimation.GREEN_FISH)