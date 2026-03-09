from typing import Tuple

from pygame import Surface, image, transform

from model.player.player import Player

# Global constants for Turtle
hitbox_width: float = 100.0
hitbox_height: float = 100.0
turtle_speed: float = 256.0
turtle_health: float = 100.0
sprite_width: float = 128.0
sprite_height: float = 128.0

class Turtle(Player):
    def __init__(self, camera_width: float, camera_height: float) -> None:
        super().__init__(camera_width, camera_height, hitbox_width, hitbox_height, turtle_speed, turtle_health)
        # Turtle Sprite info
        self._surface_left: Surface = image.load("images/baby_turtle_left.png")
        self._surface_left = self._surface_left.convert_alpha()
        self._surface_left = transform.scale(
            self._surface_left, (sprite_width, sprite_height)
        )
        self._surface_right: Surface = image.load("images/baby_turtle_right.png")
        self._surface_right = self._surface_right.convert_alpha()
        self._surface_right = transform.scale(
            self._surface_right, (sprite_width, sprite_height)
        )
        self._sprite_width_adj: float = sprite_width / 2
        self._sprite_height_adj: float = sprite_height / 2
        # HP indicator
        self._max_hp_surface: Surface = Surface((self._hitbox.width, 10.0))
        self._max_hp_surface.fill((0, 0, 0))
        self._current_hp_surface: Surface = Surface((self._hitbox.width, 10.0))
        self._current_hp_surface.fill((222, 0, 0))

    def draw(self, screen: Surface) -> None:
        # Blit the player sprite
        screen.blit(self.get_sprite(), self.get_camera_adjusted_position())
        # Blit the black max hp indicator
        hp_bar_location: Tuple[float, float] = self.get_camera_adjusted_hp_pos()
        screen.blit(self._max_hp_surface, hp_bar_location)
        # Blit the hp bar with width scaled down to the percentage of max hp the player currently has
        ratio: float = self._current_health / self._max_health
        screen.blit(
            self._current_hp_surface,
            hp_bar_location,
            (
                0,
                0,
                ratio * self._current_hp_surface.get_width(),
                self._current_hp_surface.get_height(),
            ),
        )

    def get_sprite(self) -> Surface:
        if self._facing_direction:
            return self._surface_right
        else:
            return self._surface_left

    def get_camera_adjusted_position(self) -> Tuple[float, float]:
        return (
            self._position.x - self._camera.get_window().left - self._sprite_width_adj,
            # Note: The 'bottom' attribute of a pygame rect is actually the top edge since they are drawn top down
            self._camera.get_window().bottom - self._position.y - self._sprite_height_adj,
        )

    def get_camera_adjusted_hp_pos(self) -> Tuple[float, float]:
        return (
            self._hitbox.left - self._camera.get_window().left,
            # Note: The 'bottom' attribute of a pygame rect is actually the top edge since they are drawn top down
            self._camera.get_window().bottom - self._hitbox.top - self._max_hp_surface.get_height(),
        )