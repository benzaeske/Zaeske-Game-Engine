from abc import ABC, abstractmethod

from pygame import Vector2

from model.entities.fishconfig import FishType
from model.player.camera import Camera


class PlayerInterface(ABC):
    """
    Defines publicly accessible functionality for the player.
    """
    def __init__(self):
        pass

    @abstractmethod
    def get_position(self) -> Vector2:
        """
        Gets the player's current position.
        """
        pass

    @abstractmethod
    def get_camera(self) -> Camera:
        """
        :return: A pygame Rect representing the camera at its current position.
        """
        pass

    @abstractmethod
    def update_hp(self, hp_diff: float) -> None:
        """
        Adds the provided value to the player's hp.
        """
        pass

    @abstractmethod
    def get_fish_coherency(self, fish_type: FishType) -> int:
        """
        Gets the player's current coherency with the given fish type. Coherency is the number of fish in the player's
        coherency radius.
        """
        pass
