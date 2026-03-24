from pygame import Rect, Vector2

from controller.camerainterface import CameraInterface
from model.player.playermovementlistener import PlayerMovementListener


class Camera(CameraInterface, PlayerMovementListener):
    def __init__(self, width: float, height: float) -> None:
        super().__init__()
        self._window: Rect = Rect(0, 0, width, height)
        self._width_adj: float = width / 2
        self._height_adj: float = height / 2

    def set_window_position(self, p: Vector2) -> None:
        self._window.center = p

    def get_window(self) -> Rect:
        return self._window

    def get_width(self) -> float:
        return self._window.width

    def get_height(self) -> float:
        return self._window.height

    def get_width_adj(self) -> float:
        return self._width_adj

    def get_height_adj(self) -> float:
        return self._height_adj

    def on_player_movement(self, player_position: Vector2) -> None:
        self._window.center = player_position