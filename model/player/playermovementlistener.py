from abc import ABC, abstractmethod

from pygame import Vector2


class PlayerMovementListener(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def on_player_movement(self, player_position: Vector2) -> None:
        """
        Listener actions to perform when the player moves.
        :param player_position: The new position of the player after movement.
        """
        pass