from controller.controller import GameController, ControllerOptions

world_width = 6400.0
world_height = 6400.0
cell_size = 128.0

game_controller = GameController(
    ControllerOptions(world_width, world_height, cell_size)
)

game_controller.start_game()
