from pygame import Surface

from model.entities.enemies.jellyfish import Jellyfish
from model.entities.enemies.jellyfishconfig import JellyfishConfig, JellyfishType
from model.entities.enemies.enemymanager import EnemyManager
from model.modelutils import load_sprite


class JellyfishSwarm(EnemyManager[Jellyfish]):
    """
    Implementation of EnemyManager for Jellyfish
    """
    def __init__(self, initial_cooldown: float, initial_spawn_amount: int, jellyfish_config: JellyfishConfig) -> None:
        super().__init__(initial_cooldown, initial_spawn_amount)
        self._jellyfish_config: JellyfishConfig = jellyfish_config
        self._sprite: Surface = self._load_sprite()

    def get_new_enemy(self) -> Jellyfish:
        return Jellyfish(self._sprite, self.get_manager_id(), self._jellyfish_config)

    def _load_sprite(self) -> Surface:
        match self._jellyfish_config.jellyfish_type:
            case JellyfishType.RED:
                return load_sprite("images/red_jelly.png", self._jellyfish_config.jellyfish_width,
                                   self._jellyfish_config.jellyfish_height)