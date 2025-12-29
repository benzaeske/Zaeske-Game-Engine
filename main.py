import random

from pygame import Vector2, Rect

from controller.controller import GameController, ControllerOptions
from model.entities.fish.fishsettings import FishSettings, FishType
from model.entities.jellyfish.jellyfishsettings import JellyfishSettings, JellyfishType
from model.entities.jellyfish.jellyfishspawner import JellyfishSpawner
from model.entities.school.school import School
from model.entities.school.schoolparameters import SchoolParameters
from model.world.worldspecifications import WorldSpecifications


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

world_width = 5120.0
world_height = 5120.0
cell_size = 128.0

game_controller = GameController(
    ControllerOptions(WorldSpecifications(world_width, world_height, cell_size))
)

# Create schools of fish and add to the world
spawn_region_size = 512.0

num_red_schools = 4
for _ in range(num_red_schools):

    red_school = School(
        SchoolParameters(
            128.0,
            48.0,
            1,
            1.0,
            1.8,
            1.0,
            get_random_shoal_location(
                game_controller.model.player.camera.width,
                game_controller.model.player.camera.height,
                world_height,
                world_width,
            ),
            128.0,
            1.2,
            get_random_spawn_region(
                spawn_region_size, spawn_region_size, world_width, world_height
            ),
            16,
        ),
        FishSettings(FishType.RED, 32.0, 32.0, 175.0, 30.0),
    )
    game_controller.add_school(red_school)

num_yellow_schools = 1
center_spawn_region = Rect(0, 0, game_controller.view.screen_width, game_controller.view.screen_height)
center_spawn_region.center = (int(game_controller.model.player.position.x), int(game_controller.model.player.position.y))
global_spawn_region = Rect(0, 0, world_width, world_height)
for _ in range(num_yellow_schools):
    yellow_school = School(
        SchoolParameters(
            128.0,
            48.0,
            1,
            1.0,
            1.8,
            1.0,
            None,
            1.0,
            1.0,
            center_spawn_region,
            175,
        ),
        FishSettings(FishType.YELLOW, 30.0, 30.0, 300.0, 48),
    )
    game_controller.add_school(yellow_school)


num_green_schools = 1
random_green_shoal = get_random_shoal_location(
                game_controller.model.player.camera.width,
                game_controller.model.player.camera.height,
                world_height,
                world_width,
            )
for _ in range(num_green_schools):
    green_school = School(
        SchoolParameters(
            256.0,
            96.0,
            2,
            1.0,
            1.8,
            1.0,
            Vector2(world_width / 2, 256.0),
            128.0,
            1.0,
            get_random_spawn_region(
                spawn_region_size, spawn_region_size, world_width, world_height
            ),
            32,
        ),
        FishSettings(FishType.GREEN, 48.0, 48.0, 125.0, 24),
    )
    game_controller.add_school(green_school)

jellyfish_spawner = JellyfishSpawner(
    JellyfishSettings(
        JellyfishType.RED,
        96.0,
        96.0,
        Vector2(0.0, 0.0),
        Vector2(0.0, 0.0),
        128.0,
        90,
        100,
        10
    ),
    1
)
game_controller.set_jellyfish_spawner(jellyfish_spawner)

# Start the game loop:
game_controller.start_game()
