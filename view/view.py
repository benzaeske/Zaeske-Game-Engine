import math
from typing import Tuple

import pygame
from pygame import Surface
from pygame.font import Font


class View:
    """
    The View is responsible for drawing everything on the screen using pygame functions, but should know nothing about the size or shape of the model it is drawing
    """

    def __init__(
        self,
        background_color: Tuple[int, int, int] = (0, 0, 0),
    ):
        # Screen sizing
        display_info = pygame.display.Info()
        # Display width/height currently matches world width/height and setting manually.
        # This will eventually change to only display part of the world and run at full screen
        self._display_width: int = display_info.current_w
        self._display_height: int = display_info.current_h
        self.screen: Surface = self._get_screen()
        # Get dimensions from created screen
        self.screen_width: int = self.screen.get_width()
        self.screen_height: int = self.screen.get_height()

        # Background variables
        self.background_color: Tuple[int, int, int] = background_color
        self.background: Surface = self._get_background()

        # Font
        self.font: Font = pygame.font.SysFont("Arial", 48)

        print(
            "Initialized view with pygame screen Surface dimensions: ",
            self.screen_width,
            self.screen_height,
        )
        print(
            "The actual display size used in the request was: ",
            self._display_width,
            self._display_height,
        )

    def _get_screen(self) -> Surface:
        """
        Get a full screen matching display width and height
        """
        return pygame.display.set_mode(
            (self._display_width, self._display_height), pygame.FULLSCREEN
        )

    def _get_background(self) -> Surface:
        background = pygame.Surface((self.screen_width, self.screen_height))
        background.fill(self.background_color)
        return background

    def draw_background(self, destination: Tuple[int, int] = (0, 0)) -> None:
        self.screen.blit(self.background, destination)

    def draw_surface(self, surface: Surface, dest: Tuple[float, float]) -> None:
        self.screen.blit(surface, dest)

    def print_info_to_screen(self, fps: float, player_x: int, player_y: int) -> None:
        fps_surface: Surface = self.font.render(
            str(math.floor(fps)), True, (255, 255, 255)
        )
        self.screen.blit(fps_surface, fps_surface.get_rect(x=0, y=0))
        x_surface: Surface = self.font.render(
            "x: " + str(player_x), True, (255, 255, 255)
        )
        self.screen.blit(x_surface, x_surface.get_rect(x=0, y=fps_surface.get_height()))
        y_surface: Surface = self.font.render(
            "y: " + str(player_y), True, (255, 255, 255)
        )
        self.screen.blit(
            y_surface,
            y_surface.get_rect(
                x=0, y=fps_surface.get_height() + x_surface.get_height()
            ),
        )

    @staticmethod
    def update_screen() -> None:
        pygame.display.update()
