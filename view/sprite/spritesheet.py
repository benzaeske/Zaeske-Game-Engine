from typing import Tuple

from pygame import Surface


class SpriteSheet:
    """
    Data for sprite animations. Stores a list of tuples that contain a duration and a Surface. The duration represents
    how long the associated Surface is shown in the animation.
    """
    def __init__(self, sprite_data: list[Tuple[float, Surface]]):
        self._sprite_data: list[Tuple[float, Surface]] = sprite_data

    def get_frame_duration(self, frame: int) -> float:
        """
        Returns the duration that the surface at the given frame index should be shown for.
        """
        return self._sprite_data[frame % len(self._sprite_data)][0]

    def get_sprite(self, frame: int) -> Surface:
        """
        Returns the surface at the given frame index.
        """
        return self._sprite_data[(frame % len(self._sprite_data))][1]