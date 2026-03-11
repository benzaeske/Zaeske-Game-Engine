import random

from pygame import Vector2, Rect, Surface, image, transform

from controller.controller import GameController, ControllerOptions
from view.view import WindowOptions


##########################################
# Helper functions for creating the world:
##########################################


def get_random_spawn_region(
    spawn_region_w: float,
    spawn_region_h: float,
    world_width_in: float,
    world_height_in: float,
) -> Rect:
    """
    Creates a spawn region of the specified dimensions at a random location inside the world. The spawn region generated is guaranteed to be entirely within the world.
    """
    return Rect(
        random.uniform(0, world_width_in - spawn_region_w),
        random.uniform(0, world_height_in - spawn_region_h),
        spawn_region_w,
        spawn_region_h,
    )


def get_random_shoal_location(
    camera_width: float,
    camera_height: float,
    world_width_in: float,
    world_height_in: float,
) -> Vector2:
    """
    Creates a random shoal location that is guaranteed to be within the bounds of where the player can move
    """
    return Vector2(
        random.uniform(camera_width / 2, world_width_in - (camera_width / 2)),
        random.uniform(camera_height / 2, world_height_in - (camera_height / 2)),
    )

def load_sprite(image_location: str, w, h) -> Surface:
    surface: Surface = image.load(image_location).convert_alpha()
    return transform.scale(
        surface, (w, h)
    )

########################
# Create the game world:
########################

window_options: WindowOptions = WindowOptions() # Defines the size of the display window and if fullscreen will be used
controller_options: ControllerOptions = ControllerOptions(window_options)
game_controller: GameController = GameController(controller_options)

game_controller.start_game()