from model.entities.enemyconfig import EnemyConfig


class JellyfishConfig:
    def __init__(
            self,
            enemy_config: EnemyConfig,
            scared_cell_range: int,
            scared_dist: float,
            fear_k: float
    ) -> None:
        self.enemy_config: EnemyConfig = enemy_config
        self.scared_cell_range: int = scared_cell_range
        self.scared_dist: float = scared_dist
        self.fear_k: float = fear_k