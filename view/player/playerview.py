from pygame import Surface

from model.player.player import Player
from view.sprite.spritecatalog import SpriteCatalog


class PlayerView:
    """
    Responsible for drawing the Player.
    """
    def __init__(self, player: Player, sprite_catalog: SpriteCatalog) -> None:
        self._player = player
        self._sprite_catalog = sprite_catalog

    def draw(self, screen: Surface, dt: float) -> None:
        """
        Draw the player on the provided screen.
        """
        pass

