import sys
import time
from typing import Tuple
from uuid import UUID

import pygame
from pygame.event import Event
from pygame.key import ScancodeWrapper
from pygame.time import Clock

from controller.entityconfigurations import EntityConfigurations
from controller.playerconfigurations import PlayerConfigurations
from model.entities.entityconfig import EntityConfig
from model.entities.entitytype import EntityType
from model.entities.items.shieldconfig import ShieldConfig
from model.entitymanagers.enemies.enemymanager import EnemyManager
from model.entitymanagers.fish.school import School
from controller.camera import Camera
from model.entitymanagers.items.itemmanager import ItemManager
from model.entities.items.shield import Shield
from model.player.player import Player
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from model.world.gridspace.grid_cell import GridCell
from model.world.model import Model
from view.view import View, WindowOptions


class ControllerOptions:
    def __init__(
        self,
        window_options: WindowOptions,
        grid_cell_size: float
    ) -> None:
        self.window_options: WindowOptions = window_options
        self.grid_cell_size: float = grid_cell_size


class GameController:
    """
    Top level orchestration class for managing logic loops for the game and menus. Contains a model for simulating the
    game world and entities, and a view class for drawing onto the screen.
    """
    def __init__(
        self,
        options: ControllerOptions,
    ) -> None:
        pygame.init()
        ############################
        # Initialize View and Model:
        ############################
        self._entity_configurations: EntityConfigurations = EntityConfigurations()
        self._player_configurations: PlayerConfigurations = PlayerConfigurations()
        # The View holds all logic related to drawing entities and rendering on screen
        self._view: View = View(
            options.window_options,
            self._entity_configurations.get_configs(),
            self._player_configurations.get_config()
        )
        # The Model holds the simulated world and is responsible for performing updates each frame
        self._model: Model = Model(options.grid_cell_size)
        self._model.register_entity_manager_observer(self._view)
        # Initialize the player and register on View and Model
        self._player: Player = Player(self._player_configurations.get_config()) # Eventually get config during player selection
        self._view.register_player(self._player)
        self._model.register_player(self._player)
        # Initialize the camera
        self._camera: Camera = Camera(self._view.get_screen_width(), self._view.get_screen_height())
        self._player.add_movement_listener(self._camera)
        ####################################
        # Variables for tracking game state:
        ####################################
        self._clock: Clock = pygame.time.Clock()
        self._fps: int = 60
        self._game_start_time: float = -1
        self._dt: float = 0.0
        self._mouse_pos: Tuple[int, int] = (0, 0)
        self._key_presses: ScancodeWrapper = ScancodeWrapper(())
        self._current_frame_input_events: list[Event] = []
        self._paused: bool = False

    def start_game(self):
        self._game_start_time = time.time()
        self._create_entity_managers()
        while True:
            self.do_game_loop()

    def do_game_loop(self) -> None:
        self._key_presses = pygame.key.get_pressed()
        self._mouse_pos = pygame.mouse.get_pos()
        self._current_frame_input_events = pygame.event.get()
        self.check_for_terminate()
        self.check_for_pause()
        if not self._paused:
            model_update_time = time.time()
            self.update_model()
            model_update_time = time.time() - model_update_time
            view_update_time = time.time()
            self.draw()
            view_update_time = time.time() - view_update_time
            self.fps_logging(model_update_time, view_update_time)
        self._dt = self._clock.tick(self._fps) / 1000

    def check_for_terminate(self):
        for event in self._current_frame_input_events:
            if event.type == pygame.QUIT:
                sys.exit()
        if self._key_presses[pygame.K_ESCAPE]:
            sys.exit()
        if self._player.get_current_health() <= 0.0:
            sys.exit()

    def check_for_pause(self):
        for event in self._current_frame_input_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._paused = not self._paused

    def update_model(self) -> None:
        self._model.update(self._key_presses, self._camera, self._dt)

    def draw(self) -> None:
        self.draw_background()
        camera_grid_cells: list[GridCell] = (self._model.get_model_context().grid_space
                                             .get_grid_cells_in_camera_range(self._camera))
        # Draw in a specified order:
        #  Fish
        self.draw_entities(camera_grid_cells, EntityManagerIndex.FISH)
        #  Player
        self.draw_player()
        #  Enemies
        self.draw_entities(camera_grid_cells, EntityManagerIndex.ENEMY)
        #  Items
        self.draw_entities(camera_grid_cells, EntityManagerIndex.ITEM)
        self._view.update_screen()

    def draw_background(self) -> None:
        self._view.draw_background(self._camera)

    def draw_player(self) -> None:
        self._view.draw_player(self._camera, self._dt)

    def draw_entities(self, grid_cells: list[GridCell], entity_type: EntityManagerIndex) -> None:
        """
        Draws all entities of a given type found in the provided grid cells
        :param grid_cells: The grid cells containing entities to draw.
        :param entity_type: Only entities belonging to entity managers of this type will be drawn.
        """
        manager_ids: set[UUID] = self._model.get_model_context().entity_repository.get_manager_ids(entity_type)
        for grid_cell in grid_cells:
            for entity in grid_cell.get_entities_by_manager_ids(manager_ids):
                self._view.draw_entity(entity.get_id(), self._camera, self._dt)

    def _create_entity_managers(self) -> None:
        """
        Statically creates entity managers for all entities in the game world. This will eventually be replaced with a
        more dynamic method that adds/removes entity managers throughout the game based on various factors such as
        player position, game time, world state etc
        """
        # ORDER MATTERS - Add order determines update order each frame
        self.add_items()
        self.add_enemies()
        self.add_fish()

    def add_items(self) -> None:
        item_manager: ItemManager = ItemManager()
        self._model.add_entity_manager(item_manager)
        shield_config: EntityConfig = self._entity_configurations.get_entity_config(EntityType.SHIELD)
        if not isinstance(shield_config, ShieldConfig):
            raise TypeError("Invalid shield config loaded in controller")
        item_manager.track_item(
            Shield(shield_config, item_manager.get_manager_id()),
            self._model.get_model_context(),
        )

    def add_enemies(self) -> None:
        jelly_spawn_cd: float = 5.0
        jelly_spawn_amount: int = 4

        self._model.add_entity_manager(
            EnemyManager(
                self._entity_configurations.get_entity_config(EntityType.RED_JELLYFISH),
                jelly_spawn_cd,
                jelly_spawn_amount
            )
        )

    def add_fish(self) -> None:
        num_red_schools: int = 2
        num_yellow_schools: int = 2
        num_green_schools: int = 2

        for _ in range(num_red_schools):
            school: School = School(
                self._entity_configurations.get_entity_config(EntityType.RED_FISH),
                16,
                self._model.get_model_context()
            )
            self._model.add_entity_manager(school)
            school.hatch(self._model.get_model_context())

        for _ in range(num_yellow_schools):
            school: School = School(
                self._entity_configurations.get_entity_config(EntityType.YELLOW_FISH),
                16,
                self._model.get_model_context()
            )
            self._model.add_entity_manager(school)
            school.hatch(self._model.get_model_context())

        for _ in range(num_green_schools):
            school: School = School(
                self._entity_configurations.get_entity_config(EntityType.GREEN_FISH),
                16,
                self._model.get_model_context()
            )
            self._model.add_entity_manager(school)
            school.hatch(self._model.get_model_context())

    def fps_logging(self, model_t: float, view_t: float) -> None:
        if self._dt > 0.017:
            print(
                "Frame dt was too slow to meet",
                self._fps,
                "fps. dt:",
                self._dt,
                "\nModel update time ms:",
                model_t,
                "\nView update time ms:",
                view_t,
                "\n",
            )