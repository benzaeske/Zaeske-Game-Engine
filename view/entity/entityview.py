from abc import ABC, abstractmethod
from typing import Tuple

from pygame import Surface, Rect

from model.entity.entity import Entity
from controller.camera import Camera
from view.sprite.spritecatalog import SpriteCatalog


class EntityView[T: Entity](ABC):
    """
    Responsible for drawing Entities. Contains a reference to the Entity in the Model that this class is responsible for
    drawing. Also contains a reference to the View's sprite catalog which contains preloaded sprite sheets.
    """
    def __init__(self, entity: T, sprite_catalog: SpriteCatalog):
        self._entity: T = entity
        self._sprite_catalog: SpriteCatalog = sprite_catalog

    @abstractmethod
    def draw_entity(self, screen: Surface, camera: Camera, dt: float) -> None:
        """
        Uses the sprite catalog along with information stored on this class's associated entity in order to draw it
        onto the provided screen.
        :param screen: The View screen to draw on
        :param camera: The current state of the camera from the Model
        :param dt: Delta time since the last frame in the current game loop
        """
        pass

    def to_camera_pos(self, camera: Rect, sprite_w_adj: float, sprite_h_adj: float) -> Tuple[float, float]:
        """
        Converts the represented Entity's position into coordinates relative to the Model's camera.
        :param camera: The Model's current camera
        :param sprite_w_adj: The width/2 of the sprite sheet
        :param sprite_h_adj: The height/2 of the sprite sheet
        :return: The screen coordinate to draw the represented Entity's top left corner in pygame's inverted
            y-coordinate system
        """
        return (
            self._entity.get_x() - camera.left - sprite_w_adj,
            # Note: The 'bottom' attribute of a pygame rect is actually the top edge since they are drawn top down
            camera.bottom - self._entity.get_y() - sprite_h_adj,
        )