import copy
import random

from pygame import Vector2, Surface, Rect, image, transform

from model.entities.boid import Boid
from model.entities.entity import Entity
from model.entities.fishconfig import FishConfig, FishType
from model.entitymanagers.entitymanager import EntityManager, ModelContext
from model.utils.vectorutils import limit_magnitude


class School(EntityManager):
    def __init__(self, fish_config: FishConfig, amount: int, hatch_region: Rect) -> None:
        super().__init__()
        self._fish_config: FishConfig = fish_config
        self._sprite: Surface = self._get_sprite()
        self._fish: set[Boid] = set()
        self._amount: int = amount
        self._hatch_region: Rect = hatch_region
        self._bound_w: float = 128.0 * 32 # Fish should stay bounded within a 32x32 grid-cell region relative to the player
        self._bound_w_adj: float = self._bound_w / 2
        self._bound_h: float = 128.0 * 32 # Fish should stay bounded within a 32x32 grid-cell region relative to the player
        self._bound_h_adj: float = self._bound_h / 2
        self._did_spawn: bool = False

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        if not self._did_spawn:
            # Only hatch fish once at the beginning
            self.hatch(context)
            self._did_spawn = True
        for fish in self._fish:
            fish.frame_actions(context, dt)

    def movement(self, context: ModelContext, dt: float) -> None:
        # Pre-calculated constants used for position wrapping performed in the inner loop
        min_x: float = context.player.get_position().x - self._bound_w_adj
        min_y: float = context.player.get_position().y - self._bound_h_adj
        max_x: float = context.player.get_position().x + self._bound_w_adj
        max_y: float = context.player.get_position().y + self._bound_h_adj
        w_minus_min_x: float = self._bound_w - min_x
        h_minus_min_y: float = self._bound_h - min_y
        for fish in self._fish:
            old_pos: Vector2 = copy.deepcopy(fish.get_position())
            fish.move(context, dt)
            # Wrap each fish's position to keep it inside a bounding box centered on the player's position
            if fish.get_x() < min_x or fish.get_x() > max_x:
                self.wrap_x_around_bounding_box(fish, min_x, self._bound_w, w_minus_min_x)
            if fish.get_y() < min_y or fish.get_y() > max_y:
                self.wrap_y_around_bounding_box(fish, min_y, self._bound_h, h_minus_min_y)
            # Update grid cell if necessary
            context.grid_space.process_moved_entity(old_pos, fish)

    @staticmethod
    def wrap_x_around_bounding_box(entity: Entity, min_x: float, width: float, w_minus_min_x: float) -> None:
        """
        Wraps the given Entity's x coordinate based on a rectangular boundary defined by the input parameters.
        :param entity: The entity whose position is to be wrapped.
        :param min_x: The left edge of the bounding box.
        :param width: The width of the bounding box.
        :param w_minus_min_x: A precalculated constant: width - min_x
        """
        entity.set_x(min_x + ((entity.get_x() + w_minus_min_x) % width))

    @staticmethod
    def wrap_y_around_bounding_box(entity: Entity, min_y: float, height: float, h_minus_min_y: float) -> None:
        """
        Wraps the given Entity's y coordinate based on a rectangular boundary defined by the input parameters.
        :param entity: The entity whose position is to be wrapped.
        :param min_y: The bottom edge of the bounding box.
        :param height: The height of the bounding box.
        :param h_minus_min_y: A precalculated constant: height - min_y
        """
        entity.set_y(min_y + ((entity.get_y() + h_minus_min_y) % height))

    def hatch(self, context: ModelContext) -> None:
        """
        Hatch all the fish according to this school's amount property, fish config and hatch region
        """
        for _ in range(self._amount):
            new_fish: Boid = Boid(
                self._sprite,
                self.get_manager_id(),
                self._fish_config.max_speed,
                self._fish_config.max_acceleration,
                self._fish_config.boid_config
            )
            new_fish.set_position(self._get_initial_position())
            new_fish.set_velocity(self._get_initial_velocity())
            self._fish.add(new_fish)
            context.grid_space.add_entity(new_fish)

    def _get_sprite(self) -> Surface:
        match self._fish_config.fish_type:
            case FishType.RED:
                return self.load_sprite("images/red_fish.png", self._fish_config.sprite_w, self._fish_config.sprite_h)
            case FishType.YELLOW:
                return self.load_sprite("images/yellow_fish.png", self._fish_config.sprite_w, self._fish_config.sprite_h)
            case FishType.GREEN:
                return self.load_sprite("images/green_fish.png", self._fish_config.sprite_w, self._fish_config.sprite_h)

    @staticmethod
    def load_sprite(image_location: str, w, h) -> Surface:
        surface: Surface = image.load(image_location).convert_alpha()
        return transform.scale(surface, (w, h))

    def _get_initial_position(self) -> Vector2:
        """
        Get an initial random position within the rectangular hatch region specified for this school
        """
        return Vector2(
            random.uniform(self._hatch_region.x, self._hatch_region.x + self._hatch_region.width),
            random.uniform(self._hatch_region.y, self._hatch_region.y + self._hatch_region.height),
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

    def get_fish_type(self) -> FishType:
        return self._fish_config.fish_type