from unittest import case
from uuid import UUID

import pygame
from pygame import Surface

from model.entity.enemies.jellyfish import Jellyfish
from model.entity.entity import Entity
from model.entity.entitymanagerobserver import EntityManagerObserver
from model.entity.fish.fish import Fish
from model.player.camera import Camera
from view.background import Background
from view.entity.entityview import EntityView
from view.entity.fishview import FishView
from view.entity.jellyfishview import JellyfishView
from view.sprite.spritecatalog import SpriteCatalog


class WindowOptions:
    def __init__(self, screen_width: int = None, screen_height: int = None, full_screen: bool = False) -> None:
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.full_screen: bool = full_screen
        # If nothing is passed in, default to full screen
        if self.screen_width is None and self.screen_height is None:
            self.full_screen: bool = True

class View(EntityManagerObserver):
    """
    The View is responsible for drawing everything on the screen using pygame functions, but should know nothing about the size or shape of the model it is drawing.\n
    Pygame uses an inverted y-axis which is why coordinates are being converted when coming from the model.
    """

    def __init__(self, window_options: WindowOptions) -> None:
        super().__init__()
        self._options: WindowOptions = window_options
        # Screen sizing
        display_info = pygame.display.Info()
        # Width of the display being used. Detected by pygame's built in display Info class
        self._display_width: int = display_info.current_w
        self._display_height: int = display_info.current_h
        # The screen that will be used to blit each frame
        self._screen: Surface = self._initialize_screen()
        # Get dimensions from created screen
        self._screen_width: int = self._screen.get_width()
        self._screen_height: int = self._screen.get_height()
        print(
            "Initialized view with pygame screen Surface dimensions: ",
            self._screen_width,
            self._screen_height,
        )
        self._background: Background = Background(self._display_width, self._display_height)
        self._sprite_catalog: SpriteCatalog = SpriteCatalog()
        self._entity_views: dict[UUID, EntityView] = {}

    def _initialize_screen(self) -> Surface:
        """
        Get the screen that will be used for displaying the game
        """
        if self._options.full_screen:
            return pygame.display.set_mode((self._display_width, self._display_height), pygame.FULLSCREEN)
        else:
            # Don't let the width/height exceed the maximum dimensions of the current display
            width: int = self._options.screen_width if self._options.screen_width is not None and self._options.screen_width < self._display_width else self._display_width
            height: int = self._options.screen_height if self._options.screen_height is not None and self._options.screen_height < self._display_height else self._display_height
            return pygame.display.set_mode((width, height))

    def get_screen(self) -> Surface:
        return self._screen

    def get_screen_width(self) -> int:
        return self._screen_width

    def get_screen_height(self) -> int:
        return self._screen_height

    def draw_background(self, camera: Camera) -> None:
        self._background.draw(self._screen, camera)

    @staticmethod
    def update_screen() -> None:
        pygame.display.update()

    def notify_entity_created(self, entity: Entity):
        if entity.get_id() not in self._entity_views:
            self._entity_views[entity.get_id()] = self.get_entity_view(entity)
        else:
            raise RuntimeError(f"Entity with id: {entity.get_id()} is already being tracked in View")

    def get_entity_view(self, entity: Entity) -> EntityView:
        match entity:
            case Fish():
                return FishView(entity, self._sprite_catalog)
            case Jellyfish():
                return JellyfishView(entity, self._sprite_catalog)
            case _:
                raise NotImplementedError(f"No implementation of EntityView for entity class: {entity.__class__.__name__}")

    def notify_entity_deleted(self, entity: Entity):
        self._entity_views.pop(entity.get_id(), None)