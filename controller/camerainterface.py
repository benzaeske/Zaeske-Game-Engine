from abc import ABC

from pygame import Rect


class CameraInterface(ABC):
    """
    Defines publicly accessible functionality for the camera.
    """
    def __init__(self) -> None:
        pass

    def get_window(self) -> Rect:
        """
        :return: the rectangular camera window at its current position
        """
        pass

    def get_width(self) -> float:
        """
        :return: width of the camera window
        """
        pass

    def get_height(self) -> float:
        """
        :return: height of the camera window
        """
        pass

    def get_width_adj(self) -> float:
        """
        :return: Precalculated constant for width adjustment (width / 2)
        """
        pass

    def get_height_adj(self) -> float:
        """
        :return: Precalculated constant for height adjustment (height / 2)
        """
        pass