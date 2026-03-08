from abc import ABC, abstractmethod

from pygame import Vector2

from model.entities.fishconfig import FishType


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
    def update_hp(self, n: float) -> None:
        """
        Adds the provided value to the player's hp.
        """
        pass

    @abstractmethod
    def get_fish_coherency(self, fish_type: FishType) -> int:
        """
        Gets the player's current coherency with the given fish type. Coherency is the number of fish in player's
        coherency radius.
        """
        pass
