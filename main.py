from controller.controller import GameController, ControllerOptions
from view.view import WindowOptions

#############################
# Create the game Controller:
#############################

# Defines the size of the display window and if fullscreen will be used
window_options: WindowOptions = WindowOptions()
# Determines the size of grid cells in the spatial partitioning model
grid_cell_size: float = 128.0

controller_options: ControllerOptions = ControllerOptions(window_options, grid_cell_size)
game_controller: GameController = GameController(controller_options)

###############
# Ready set go!
###############
game_controller.start_game()