from pygame import Surface, Vector2, Rect

from model.utils.vectorutils import limit_magnitude, safe_normalize


class GameEntity:

    def __init__(
        self,
        sprite: Surface,
        sprite_width: float = 1.0,
        sprite_height: float = 1.0,
        hitbox_width: float = 0.0,
        hitbox_height: float = 0.0,
        start_pos: Vector2 = Vector2(0.0, 0.0),
        start_v: Vector2 = Vector2(0.0, 0.0),
        max_speed: float = 1.0,
        max_acceleration: float = 0.1,
    ):
        # The sprite is what is drawn on screen.
        # The width and height adjusts are for easy calculations when converting the model coordinates to screen coordinates when drawing
        self.sprite: Surface = sprite
        self.sprite_width_adj: float = sprite_width / 2
        self.sprite_height_adj: float = sprite_height / 2
        self.position: Vector2 = start_pos
        # The hitbox is how big the entity actually is when performing hit detection.
        # The sprite and the hitbox are on top of each other's centers
        self.hitbox: Rect = Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = (int(self.position.x), int(self.position.y))
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
        self.hitbox.center = (int(self.position.x), int(self.position.y))

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
        return self.sprite
