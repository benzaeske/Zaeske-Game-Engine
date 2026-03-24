from abc import ABC, abstractmethod

from pygame import Vector2


class PlayerMovementListener(ABC):
    """
    Listener pattern for classes that need to define some set of functionality when the player moves. Must be registered
    to the current active Player using Player.add_movement_listener
    """
    def __init__(self):
        pass

    @abstractmethod
    def on_player_movement(self, player_position: Vector2) -> None:
        """
        Listener actions to perform when the player moves.
        :param player_position: The new position of the player after movement.
        """
        pass