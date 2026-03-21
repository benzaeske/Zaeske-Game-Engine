from typing import Tuple

from pygame import Surface

from model.player.camera import Camera
from model.player.playerinterface import PlayerInterface
from view.sprite.playeranimation import PlayerAnimation
from view.sprite.spritecatalog import SpriteCatalog
from view.sprite.spritesheet import SpriteSheet


class PlayerView:
    """
    Responsible for drawing the Player.
    """
    def __init__(self, player: PlayerInterface, sprite_catalog: SpriteCatalog) -> None:
        self._player: PlayerInterface = player
        self._sprite_catalog: SpriteCatalog = sprite_catalog
        # Current facing direction of the player
        self._facing_direction: int = 1
        # HP indicator. Should be moved to its own class eventually
        self._max_hp_surface: Surface = Surface((self._player.get_hitbox().width, 10.0))
        self._max_hp_surface.fill((0, 0, 0))
        self._current_hp_surface: Surface = Surface((self._player.get_hitbox().width, 10.0))
        self._current_hp_surface.fill((222, 0, 0))

    def draw(self, screen: Surface, camera: Camera, dt: float) -> None:
        """
        Draw the player on the provided screen.
        :param screen: The screen from the View to draw the player on.
        :param camera: The current Camera object
        :param dt: The time delta between frames. Will eventually be used to track animation frame timings.
        """
        self._update_facing_direction()
        animation_state: PlayerAnimation = self.get_animation_state()
        sprite_sheet: SpriteSheet = self._sprite_catalog.get_player_animation(animation_state)
        screen.blit(
            sprite_sheet.get_sprite(0), # currently only have static sprite sheets with one animation frame
            self._get_camera_adjusted_position(camera, sprite_sheet)
        )
        self._draw_hp_indicator(screen, camera)

    def _update_facing_direction(self) -> None:
        if self._player.get_acceleration().x != 0:
            if self._player.get_acceleration().x > 0:
                self._facing_direction = 1
            else:
                self._facing_direction = 0

    def get_animation_state(self) -> PlayerAnimation:
        """
        Gets the animation state of the player for this frame
        """
        match self._facing_direction:
            case 0:
                return PlayerAnimation.SWIMMING_LEFT
            case 1:
                return PlayerAnimation.SWIMMING_RIGHT
            case _:
                raise ValueError(f"Invalid facing direction: {self._facing_direction}")

    def _draw_hp_indicator(self, screen: Surface, camera: Camera) -> None:
        """
        Draw the hp bar at the bottom of the player's hitbox. A black rectangle is drawn first with full width and then
        a red rectangle is drawn with width scaled to the ratio of the player's current hp to max hp.
        """
        hp_bar_location: Tuple[float, float] = self._get_camera_adjusted_hp_pos(camera)
        screen.blit(self._max_hp_surface, hp_bar_location)
        # Blit the current hp with width scaled down to the percentage of max hp the player currently has
        ratio: float = self._player.get_current_health() / self._player.get_max_health()
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

    def _get_camera_adjusted_position(self, camera: Camera, sprite_sheet: SpriteSheet) -> Tuple[float, float]:
        return (
            self._player.get_position().x - camera.get_window().left - sprite_sheet.get_width_adj(),
            # Note: The 'bottom' attribute of a pygame rect is actually the top edge since they are drawn top down
            camera.get_window().bottom - self._player.get_position().y - sprite_sheet.get_height_adj(),
        )

    def _get_camera_adjusted_hp_pos(self, camera: Camera) -> Tuple[float, float]:
        return (
            self._player.get_hitbox().left - camera.get_window().left,
            # Note: The 'bottom' attribute of a pygame rect is actually the top edge since they are drawn top down
            camera.get_window().bottom - self._player.get_hitbox().top - self._max_hp_surface.get_height(),
        )