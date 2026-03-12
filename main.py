from controller.controller import GameController, ControllerOptions
from view.view import WindowOptions

########################
# Create the game world:
########################

window_options: WindowOptions = WindowOptions() # Defines the size of the display window and if fullscreen will be used
controller_options: ControllerOptions = ControllerOptions(window_options)
game_controller: GameController = GameController(controller_options)

###############
# Ready set go!
###############
game_controller.start_game()