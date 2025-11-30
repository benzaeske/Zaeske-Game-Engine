from pygame import Surface, Vector2

from model.utils.vectorutils import limit_magnitude, safe_normalize


class GameEntity:

    def __init__(
        self,
        surface: Surface,
        width: float = 1.0,
        height: float = 1.0,
        start_pos: Vector2 = Vector2(0.0, 0.0),
        start_v: Vector2 = Vector2(0.0, 0.0),
        max_speed: float = 1.0,
        max_acceleration: float = 0.1,
    ):
        self.surface: Surface = surface
        self.width: float = width
        self.height: float = height

        # Physics-related variables:
        self.position: Vector2 = start_pos
        self.velocity: Vector2 = start_v
        self.acceleration: Vector2 = Vector2(0.0, 0.0)
        self.max_speed: float = max_speed
        self.max_acceleration: float = max_acceleration

    def update_position(self, world_w: float, world_h: float, dt: float) -> None:
        """
        Updates entities for a single frame.\n
        All coordinates are assumed to represent the center of entities and have an inverted y-axis\n
        By default, an entity's acceleration is set back to 0 after its position is updated
        """
        self.velocity += self.acceleration
        limit_magnitude(self.velocity, self.max_speed)
        self.position += self.velocity * dt
        self.position.x = (self.position.x + world_w) % world_w
        self.position.y = (self.position.y + world_h) % world_h
        self.acceleration *= 0.0

    def target(self, target_dir: Vector2, k: float) -> None:
        """
        Accelerates this entity in the target direction.
        """
        safe_normalize(target_dir)
        target_dir *= self.max_speed
        target_dir -= self.velocity
        limit_magnitude(target_dir, self.max_acceleration)
        target_dir *= k
        self.acceleration += target_dir

    def get_surface(self):
        return self.surface
