class EnemyConfig:
    """
    Parameters used to construct a basic Enemy entity
    """
    def __init__(
            self,
            max_speed: float,
            max_acceleration: float,
            hitbox_width: float,
            hitbox_height: float,
            hp: int,
            damage: int,
            neighbor_cell_range: int,
            avoid_neighbor_dist: float,
            avoid_neighbor_k: float
    ) -> None:
        """
        :param max_speed: Maximum speed of the enemy
        :param max_acceleration: Maximum acceleration that the enemy can act on itself with
        :param hitbox_width: Width of the enemy's hitbox
        :param hitbox_height: Height of the enemy's hitbox
        :param hp: Hit points
        :param damage: Damage inflicted by the enemy
        :param avoid_neighbor_dist: The range at which this enemy will avoid its neighbors
        :param neighbor_cell_range: The range of grid cells to check for neighbors - based off avoid distance
        :param avoid_neighbor_k: How strongly the enemy will prioritize avoiding its neighbors
        """
        self.max_speed = max_speed
        self.max_acceleration = max_acceleration
        self.hitbox_width = hitbox_width
        self.hitbox_height = hitbox_height
        self.hp = hp
        self.damage = damage
        self.neighbor_cell_range = neighbor_cell_range
        self.avoid_neighbor_dist = avoid_neighbor_dist
        self.avoid_neighbor_k = avoid_neighbor_k