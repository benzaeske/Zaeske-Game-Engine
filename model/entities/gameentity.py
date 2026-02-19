import copy
import uuid

from pygame import Surface, Vector2, Rect

from model.utils.vectorutils import limit_magnitude, safe_normalize


class GameEntity:

    def __init__(
        self,
        group_id: uuid.UUID,
        sprite: Surface,
        hitbox_width: float,
        hitbox_height: float,
        max_speed: float,
        max_acceleration: float,
        start_pos: Vector2 = Vector2(0.0, 0.0),
        start_v: Vector2 = Vector2(0.0, 0.0)
    ):
        self.entity_id: uuid.UUID = uuid.uuid4()
        self.group_id: uuid.UUID = group_id
        # The sprite is what is drawn on screen.
        # The width and height adjusts are for easy calculations when converting the model coordinates to screen coordinates when drawing
        self.sprite: Surface = sprite
        self.sprite_width_adj: float = sprite.get_width() / 2
        self.sprite_height_adj: float = sprite.get_height() / 2
        self.position: Vector2 = copy.deepcopy(start_pos)
        # The hitbox is how big the entity actually is when performing hit detection.
        # The sprite and the hitbox are on top of each other's centers
        self.hitbox: Rect = Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = (int(self.position.x), int(self.position.y))
        self.velocity: Vector2 = copy.deepcopy(start_v)
        self.acceleration: Vector2 = Vector2(0.0, 0.0)
        self.max_speed: float = max_speed
        self.max_acceleration: float = max_acceleration

    def update_position(self, world_w: float, world_h: float, dt: float) -> None:
        """
        Updates this entity's position for a single frame by applying acceleration to the entity's current velocity,
        then applying the updated velocity scaled to delta time (dt) to the entity's position.\n
        By default, an entity's acceleration is set back to 0 after its position is updated
        """
        self.velocity += (self.acceleration * dt)
        limit_magnitude(self.velocity, self.max_speed)
        self.position += self.velocity * dt
        self.position.x = (self.position.x + world_w) % world_w
        if self.position.y < 0:
            self.position.y = 0
        if self.position.y >= world_h:
            self.position.y = world_h - 1
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

    def get_surface(self) -> Surface:
        return self.sprite

    def __eq__(self, other):
        return self.entity_id == other.entity_id

    def __hash__(self):
        return hash(self.entity_id)


