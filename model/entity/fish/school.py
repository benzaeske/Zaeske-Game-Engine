import copy
import random

from pygame import Vector2, Surface, Rect

from model.entity.fish.fish import Fish
from model.entity.fish.fishconfig import FishConfig, FishType
from model.entity.entitymanager import EntityManager, ModelContext
from model.modelutils import limit_magnitude, load_sprite


class School(EntityManager):
    def __init__(self, fish_config: FishConfig, amount: int, context: ModelContext) -> None:
        super().__init__()
        self._fish_config: FishConfig = fish_config
        self._sprite: Surface = self._get_sprite()
        self._amount: int = amount
        self._fish: set[Fish] = set()
        # The school has a boundary within a certain range of the player
        self._boundary_w: float = 128.0 * 32
        self._boundary_h: float = 128.0 * 32
        self._boundary: Rect = Rect((0, 0), (self._boundary_w, self._boundary_h))
        self._boundary.center = context.player.get_position()
        self._shoal: Rect | None = Rect((0, 0), (self._fish_config.shoal_radius * 2, self._fish_config.shoal_radius * 2)) if self._fish_config.shoal else None
        self._shoal.center = self.get_random_shoal_location()
        # Hatch fish once at the beginning
        self.hatch(context)

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        self._boundary.center = context.player.get_position()
        if self._fish_config.shoal:
            # Move the shoal location if it is outside the school's boundary
            if not self._boundary.collidepoint(self._shoal.center):
                self._randomize_shoal_location()
        for fish in self._fish:
            fish.frame_actions(context, dt)

    def movement(self, context: ModelContext, dt: float) -> None:
        for fish in self._fish:
            old_pos: Vector2 = copy.deepcopy(fish.get_position())
            fish.move(context, dt)
            # Teleport fish back inside their shoal if they go outside the school's boundary and the shoal is not in camera range
            if (not self._boundary.collidepoint(fish.get_position()) and
                    not context.player.get_camera().get_window().colliderect(self._shoal)):
                fish.set_position(self._get_random_position_inside_shoal())
            # Update grid cell if necessary
            context.grid_space.process_moved_entity(old_pos, fish)

    def hatch(self, context: ModelContext) -> None:
        """
        Hatch all the fish according to this school's amount property, fish config and hatch region
        """
        for _ in range(self._amount):
            new_fish: Fish = Fish(
                self.get_manager_id(),
                self._fish_config,
                self._sprite,
                self._shoal
            )
            new_fish.set_position(self._get_random_position_inside_shoal())
            new_fish.set_velocity(self._get_initial_velocity())
            self._fish.add(new_fish)
            context.grid_space.add_entity(new_fish)

    def _get_random_position_inside_shoal(self) -> Vector2:
        """
        Get an initial random position within the school's shoal
        """
        return Vector2(
            random.uniform(self._shoal.left, self._shoal.right),
            random.uniform(self._shoal.top, self._shoal.bottom),
        )

    def _get_initial_velocity(self) -> Vector2:
        """
        Create an initial velocity vector in a random direction with a magnitude capped at the max speed specified on
        this school's fish config.
        """
        max_speed: float = self._fish_config.max_speed
        initial_velocity = Vector2(
            random.uniform(-max_speed, max_speed),
            random.uniform(-max_speed, max_speed),
        )
        limit_magnitude(initial_velocity, max_speed)
        return initial_velocity

    def get_random_shoal_location(self) -> Vector2:
        return Vector2(
            random.uniform(self._boundary.left, self._boundary.right),
            random.uniform(self._boundary.top, self._boundary.bottom)
        )

    def _randomize_shoal_location(self):
        self._shoal.centerx = random.uniform(self._boundary.left, self._boundary.right)
        self._shoal.centery = random.uniform(self._boundary.top, self._boundary.bottom)

    def _get_sprite(self) -> Surface:
        match self._fish_config.fish_type:
            case FishType.RED:
                return load_sprite("images/red_fish.png", self._fish_config.sprite_w, self._fish_config.sprite_h)
            case FishType.YELLOW:
                return load_sprite("images/yellow_fish.png", self._fish_config.sprite_w, self._fish_config.sprite_h)
            case FishType.GREEN:
                return load_sprite("images/green_fish.png", self._fish_config.sprite_w, self._fish_config.sprite_h)

    def get_fish_type(self) -> FishType:
        return self._fish_config.fish_type