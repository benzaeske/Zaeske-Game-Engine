from model.entities.enemies.jellyfish import Jellyfish
from model.entities.enemies.jellyfishconfigv1 import JellyfishConfigV1
from model.entitymanagers.enemies.enemymanager import EnemyManager


class JellyfishSwarm(EnemyManager[Jellyfish]):
    # TODO this class is obsolete. EnemyManager should create enemies using EnemyType/EnemyConfigs
    """
    Implementation of EnemyManager for Jellyfish
    """
    def __init__(self, initial_cooldown: float, initial_spawn_amount: int, jellyfish_config: JellyfishConfigV1) -> None:
        super().__init__(initial_cooldown, initial_spawn_amount)
        self._jellyfish_config: JellyfishConfigV1 = jellyfish_config

    def get_new_enemy(self) -> Jellyfish:
        return Jellyfish(self.get_manager_id(), self._jellyfish_config)