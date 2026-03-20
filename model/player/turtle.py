from model.player.camera import Camera
from model.player.player import Player

# Global constants for Turtle
hitbox_width: float = 100.0
hitbox_height: float = 100.0
turtle_speed: float = 256.0
turtle_health: float = 100.0

class Turtle(Player):
    def __init__(self, camera: Camera) -> None:
        super().__init__(camera, hitbox_width, hitbox_height, turtle_speed, turtle_health)