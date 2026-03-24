from typing import Tuple

from pygame import Surface


class SpriteSheet:
    """
    Data for sprite animations. Stores a list of tuples that contain a duration and a Surface. The duration represents
    how long the associated Surface is shown in the animation.
    """
    def __init__(self, sprite_data: list[Tuple[float, Surface]], width: float, height: float) -> None:
        """
        :param sprite_data: Tuples containing duration and surfaces for the sprite animation. The surfaces provided in
            sprite data are assumed to all have the same height and width as specified in the constructor.
        :param width: The width of all surfaces in the animation
        :param height: The height of all surfaces passed in the animation
        """
        self._sprite_data: list[Tuple[float, Surface]] = sprite_data
        self._num_animation_frames: int = len(self._sprite_data)
        self._width: float = width
        self._height: float = height
        self._width_adj: float = width / 2
        self._height_adj: float = height / 2

    def get_frame_duration(self, frame: int) -> float:
        """
        Returns the duration that the surface at the given frame index should be shown for.
        """
        return self._sprite_data[frame % len(self._sprite_data)][0]

    def get_num_frames(self) -> int:
        return self._num_animation_frames

    def get_sprite(self, frame: int) -> Surface:
        """
        Returns the surface at the given frame index.
        """
        return self._sprite_data[(frame % len(self._sprite_data))][1]

    def get_width(self) -> float:
        return self._width

    def get_height(self) -> float:
        return self._height

    def get_width_adj(self) -> float:
        return self._width_adj

    def get_height_adj(self) -> float:
        return self._height_adj