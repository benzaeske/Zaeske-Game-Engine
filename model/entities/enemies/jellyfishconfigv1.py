from enum import Enum

from model.entities.enemies.enemyconfigv1 import EnemyConfigV1

class JellyfishType(Enum):
    RED = 0

class JellyfishConfigV1:
    def __init__(
            self,
            jellyfish_type: JellyfishType,
            jellyfish_width: float,
            jellyfish_height: float,
            enemy_config: EnemyConfigV1,
            scared_cell_range: int,
            scared_dist: float,
            fear_k: float
    ) -> None:
        self.jellyfish_type: JellyfishType = jellyfish_type
        self.jellyfish_width: float = jellyfish_width
        self.jellyfish_height: float = jellyfish_height
        self.enemy_config: EnemyConfigV1 = enemy_config
        self.scared_cell_range: int = scared_cell_range
        self.scared_dist: float = scared_dist
        self.fear_k: float = fear_k