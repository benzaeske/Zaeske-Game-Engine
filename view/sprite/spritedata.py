from pygame import Surface


class SpriteData:
    """
    Stores data for a single sprite that may or may not be part of a larger sprite sheet animation.
    """
    def __init__(self, surface: Surface) -> None:
        self._surface: Surface = surface
        self._width_adj: int = int(self._surface.get_width() / 2)
        self._height_adj: int = int(self._surface.get_height() / 2)

    def get_surface(self) -> Surface:
        return self._surface

    def get_width_adj(self) -> int:
        return self._width_adj

    def get_height_adj(self) -> int:
        return self._height_adj