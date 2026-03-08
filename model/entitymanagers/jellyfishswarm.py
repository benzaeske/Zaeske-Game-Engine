from pygame import Surface

from model.entities.enemy import Enemy
from model.entities.enemyconfig import EnemyConfig
from model.entities.jellyfish import Jellyfish
from model.entities.jellyfishconfig import JellyfishConfig
from model.entitymanagers.enemymanager import EnemyManager
from model.entitymanagers.entitymanager import ModelContext
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex


class JellyfishSwarm(EnemyManager[Jellyfish]):
    """
    Implementation of EnemyManager for Jellyfish
    """
    def __init__(self, initial_cooldown: float, initial_amount: int, jellyfish_config: JellyfishConfig, sprite: Surface) -> None:
        super().__init__(initial_cooldown, initial_amount)
        self._jellyfish_config: JellyfishConfig = jellyfish_config
        self._sprite: Surface = sprite

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        super().frame_actions(context, dt)
        for jellyfish in self._enemies:
            jellyfish.avoid_fish(
                self._jellyfish_config,
                context.grid_space.get_entity_neighbors(
                    jellyfish,
                    self._jellyfish_config.scared_cell_range,
                    context.get_manager_ids_by_type(EntityManagerIndex.RED_FISH)
                ),
                context.get_world_width()
            )

    def get_new_enemy(self) -> Enemy:
        return Jellyfish(self._sprite, self.get_manager_id(), self._jellyfish_config.enemy_config)

    def get_enemy_config(self) -> EnemyConfig:
        return self._jellyfish_config.enemy_config