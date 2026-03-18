from abc import ABC, abstractmethod

from pygame import Surface

from model.entity.entity import Entity
from model.player.camera import Camera
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
    def draw_entity(self, screen: Surface, camera: Camera) -> None:
        """
        Uses the sprite catalog along with information stored on this class's associated entity in order to draw it
        onto the provided screen.
        :param screen: The View screen to draw on
        :param camera: The current state of the camera from the Model
        """
        pass