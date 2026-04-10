from abc import ABC, abstractmethod

from pygame import Vector2, Rect

from model.entities.entitytype import EntityType


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
    def get_velocity(self) -> Vector2:
        """
        Gets the player's current velocity.
        """
        pass

    @abstractmethod
    def get_acceleration(self) -> Vector2:
        """
        Gets the player's current acceleration.
        """
        pass

    @abstractmethod
    def get_hitbox(self) -> Rect:
        """
        Gets the player's hitbox.
        """
        pass

    @abstractmethod
    def get_current_health(self) -> float:
        """
        Gets the player's current hp.
        """
        pass

    @abstractmethod
    def get_max_health(self) -> float:
        """
        Gets the player's maximum hp.
        """
        pass

    @abstractmethod
    def update_health(self, hp_diff: float) -> None:
        """
        Adds the provided value to the player's hp. Values can be negative.
        """
        pass

    @abstractmethod
    def get_fish_coherency(self, fish_type: EntityType) -> int:
        """
        Gets the player's current coherency with the given fish type. Coherency is the number of fish in the player's
        coherency radius.
        """
        pass