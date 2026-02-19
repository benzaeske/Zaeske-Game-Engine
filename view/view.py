import math
from typing import Tuple

import pygame
from pygame import Surface, Rect


class WindowOptions:
    def __init__(self, screen_width: int = None, screen_height: int = None, full_screen: bool = False) -> None:
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.full_screen: bool = full_screen
        # If nothing is passed in, default to full screen
        if self.screen_width is None and self.screen_height is None:
            self.full_screen: bool = True

class View:
    """
    The View is responsible for drawing everything on the screen using pygame functions, but should know nothing about the size or shape of the model it is drawing.\n
    Pygame uses an inverted y-axis which is why coordinates are being converted when coming from the model.
    """

    def __init__(self, options: WindowOptions) -> None:
        self.options: WindowOptions = options
        # Screen sizing
        display_info = pygame.display.Info()
        # Width the display being used as detected by pygame's built in display Info class
        self._display_width: int = display_info.current_w
        self._display_height: int = display_info.current_h
        # The screen that will be used to blit each frame
        self.screen: Surface = self._get_screen()
        # Get dimensions from created screen
        self.screen_width: int = self.screen.get_width()
        self.screen_height: int = self.screen.get_height()

        # Font
        #self.font: Font = pygame.font.SysFont("Arial", 48)

        print(
            "Initialized view with pygame screen Surface dimensions: ",
            self.screen_width,
            self.screen_height,
        )

    def _get_screen(self) -> Surface:
        """
        Get the screen that will be used for displaying the game
        """
        if self.options.full_screen:
            return pygame.display.set_mode((self._display_width, self._display_height), pygame.FULLSCREEN)
        else:
            # Don't let the width/height exceed the maximum dimensions of the current display
            width: int = self.options.screen_width if self.options.screen_width is not None and self.options.screen_width < self._display_width else self._display_width
            height: int = self.options.screen_height if self.options.screen_height is not None and self.options.screen_height < self._display_height else self._display_height
            return pygame.display.set_mode((width, height))

    def draw_surface(self, surface: Surface, dest: Tuple[float, float], area: Tuple[float, float, float, float] | None = None) -> None:
        self.screen.blit(surface, dest, area)

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
