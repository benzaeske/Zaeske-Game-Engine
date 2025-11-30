import random

from pygame import Vector2, Rect

from controller.controller import GameController, ControllerOptions
from model.entities.fish.fishsettings import FishSettings, FishType
from model.entities.school.school import School
from model.entities.school.schoolparameters import SchoolParameters


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


########################
# Create the game world:
########################

world_width = 6400.0
world_height = 6400.0
cell_size = 128.0

game_controller = GameController(
    ControllerOptions(world_width, world_height, cell_size)
)

# Create schools of fish and add to the world

shoal_radius = 128.0
spawn_region_size = 512.0
red_school = School(
    SchoolParameters(
        128.0,
        48.0,
        1,
        1.0,
        1.8,
        1.0,
        get_random_shoal_location(
            game_controller.model.player.camera_width,
            game_controller.model.player.camera_height,
            world_height,
            world_width,
        ),
        shoal_radius,
        1.0,
        Rect(
            world_width / 2.0, world_height / 2.0, spawn_region_size, spawn_region_size
        ),
        32,
    ),
    FishSettings(FishType.RED, 32.0, 32.0, 200.0, 0.5),
)
game_controller.add_school(red_school)


# Start the game loop:
game_controller.start_game()
