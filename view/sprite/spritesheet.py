from typing import Tuple

from pygame import Surface


def from_sprite(sprite: Surface) -> AnimatedSprite:
    """
    Quick helper method for constructing an instance of AnimatedSprite when only a single animation surface exists.
    """
    return AnimatedSprite([(1.0, sprite)])


class AnimatedSprite:
    """
    Stores a list of tuples that contain a duration and a Surface. The duration represents how long the given Surface is
    shown in the animation. An internal timer tracks which animation surface is returned when get_sprite is called.
    """
    def __init__(self, sprite_catalog: list[Tuple[float, Surface]]):
        self._sprite_catalog: list[Tuple[float, Surface]] = sprite_catalog
        self._current_sprite_index: int = 0
        self._timer: float = 0.0

    def update(self, dt: float) -> None:
        """
        Updates this animation's internal timer. Changes the active sprite based on the animation timer if needed. This
        method should only be called once per frame of the main game loop.
        :param dt: Delta time since the last frame
        """
        self._timer += dt
        if self._timer >= self._sprite_catalog[self._current_sprite_index][0]:
            self._current_sprite_index += 1
            self._current_sprite_index %= len(self._sprite_catalog)
            self._timer = 0.0

    def get_sprite(self) -> Surface:
        """
        Returns the sprite that should be shown according to the internal animation timer. Timer can only be updated
        using the update method.
        """
        return self._sprite_catalog[self._current_sprite_index][1]