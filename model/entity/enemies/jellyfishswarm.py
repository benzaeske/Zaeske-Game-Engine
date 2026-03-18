from model.entity.enemies.jellyfish import Jellyfish
from model.entity.enemies.jellyfishconfig import JellyfishConfig
from model.entity.enemies.enemymanager import EnemyManager


class JellyfishSwarm(EnemyManager[Jellyfish]):
    """
    Implementation of EnemyManager for Jellyfish
    """
    def __init__(self, initial_cooldown: float, initial_spawn_amount: int, jellyfish_config: JellyfishConfig) -> None:
        super().__init__(initial_cooldown, initial_spawn_amount)
        self._jellyfish_config: JellyfishConfig = jellyfish_config

    def get_new_enemy(self) -> Jellyfish:
        return Jellyfish(self.get_manager_id(), self._jellyfish_config)