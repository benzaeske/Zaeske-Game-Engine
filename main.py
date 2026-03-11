from controller.controller import GameController, ControllerOptions
from model.entities.enemyconfig import EnemyConfig
from model.entities.jellyfishconfig import JellyfishConfig, JellyfishType
from model.entitymanagers.jellyfishswarm import JellyfishSwarm
from view.view import WindowOptions

########################
# Create the game world:
########################

window_options: WindowOptions = WindowOptions() # Defines the size of the display window and if fullscreen will be used
controller_options: ControllerOptions = ControllerOptions(window_options)
game_controller: GameController = GameController(controller_options)

# Add Red Jellyfish:
jelly_spawn_cd: float = 5.0
jelly_spawn_amount: int = 4
jelly_config: JellyfishConfig = JellyfishConfig(
    JellyfishType.RED,
    96.0,
    96.0,
    EnemyConfig(
        128.0,
        90.0,
        96.0,
        96.0,
        100,
        10,
        1,
        96.0,
        2.0
    ),
    2,
    192.0,
    3.0
)
jelly_swarm: JellyfishSwarm = JellyfishSwarm(jelly_spawn_cd, jelly_spawn_amount, jelly_config)
game_controller.add_entity_manager(jelly_swarm)

###############
# Ready set go!
###############
game_controller.start_game()