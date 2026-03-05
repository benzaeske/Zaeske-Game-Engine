from pygame import Surface

from model.entities.enemy import Enemy
from model.entities.jellyfish import Jellyfish
from model.entities.jellyfishconfig import JellyfishConfig
from model.entitygroups.enemygroup import EnemyGroup


class JellyFishSwarm(EnemyGroup):
    """
    Implementation of EnemyGroup that spawns jellyfish
    """
    def __init__(self, initial_cooldown: float, initial_amount: int, jellyfish_config: JellyfishConfig, sprite: Surface) -> None:
        super().__init__(initial_cooldown, initial_amount)
        self._jellyfish_config: JellyfishConfig = jellyfish_config
        self._sprite: Surface = sprite

    def get_new_enemy(self) -> Enemy:
        return Jellyfish(self._sprite, self.get_group_id(), self._jellyfish_config)

