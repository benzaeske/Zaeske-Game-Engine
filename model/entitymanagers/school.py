import copy
import random

from pygame import Vector2, Surface, Rect

from model.entities.entity import Entity
from model.entities.fish import Fish
from model.entities.fishconfig import FishConfig, FishType
from model.entitymanagers.entitymanager import EntityManager, ModelContext
from model.modelutils import limit_magnitude, load_sprite


class School(EntityManager):
    def __init__(self, fish_config: FishConfig, amount: int, context: ModelContext) -> None:
        super().__init__()
        self._fish_config: FishConfig = fish_config
        self._sprite: Surface = self._get_sprite()
        self._amount: int = amount
        self._fish: set[Fish] = set()
        # Fish should stay bounded within a 48x48 grid-cell region relative to the player
        self._fish_bound_w: float = 128.0 * 48
        self._fish_bound_h: float = 128.0 * 48
        self._fish_boundary: Rect = Rect((0, 0), (self._fish_bound_w, self._fish_bound_h))
        self._fish_boundary.center = context.player.get_position()
        self._hatch_region = self.generate_hatch_region()
        # The school's shoaling location should be bounded within a 48x48 grid-cell region relative to the player
        self._shoal_boundary: Rect = Rect((0, 0), (128.0 * 48, 128.0 * 48))
        self._shoal_boundary.center = context.player.get_position()
        self._shoal_location: Vector2 | None = self.get_random_shoal_location() if self._fish_config.shoal else None
        # Hatch fish once when the school is instantiated
        self.hatch(context)

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        self._fish_boundary.center = context.player.get_position()
        self._shoal_boundary.center = context.player.get_position()
        if self._fish_config.shoal:
            # Move the shoal location if it is outside the shoaling boundary
            if not self._shoal_boundary.collidepoint(self._shoal_location):
                self._shoal_location = self.get_random_shoal_location()
        for fish in self._fish:
            fish.frame_actions(context, dt)

    def movement(self, context: ModelContext, dt: float) -> None:
        # Pre-calculated constants used for position wrapping performed in the inner loop
        w_minus_min_x: float = self._fish_bound_w - self._fish_boundary.left
        h_minus_min_y: float = self._fish_bound_h - self._fish_boundary.top
        for fish in self._fish:
            old_pos: Vector2 = copy.deepcopy(fish.get_position())
            fish.move(context, dt)
            # Wrap each fish's position to keep it inside a bounding box centered on the player's position
            if fish.get_x() < self._fish_boundary.left or fish.get_x() > self._fish_boundary.right:
                self.wrap_x_around_bounding_box(fish, self._fish_boundary.left, self._fish_bound_w, w_minus_min_x)
            if fish.get_y() < self._fish_boundary.top or fish.get_y() > self._fish_boundary.bottom:
                self.wrap_y_around_bounding_box(fish, self._fish_boundary.top, self._fish_bound_h, h_minus_min_y)
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
            new_fish: Fish = Fish(
                self._sprite,
                self.get_manager_id(),
                self._fish_config,
                self._shoal_location
            )
            new_fish.set_position(self._get_initial_position())
            new_fish.set_velocity(self._get_initial_velocity())
            self._fish.add(new_fish)
            context.grid_space.add_entity(new_fish)

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

    def generate_hatch_region(self) -> Rect:
        """
        Generate a random hatch region within the boundary of this school
        """
        hatch_region_size: float = self._fish_config.hatch_radius
        hatch_region: Rect = Rect(
            (
                random.uniform(self._fish_boundary.left, self._fish_boundary.right - hatch_region_size),
                random.uniform(self._fish_boundary.top, self._fish_boundary.bottom - hatch_region_size)
            ),
            (
                hatch_region_size,
                hatch_region_size
            )
        )
        return hatch_region

    def get_random_shoal_location(self) -> Vector2:
        return Vector2(
            random.uniform(self._shoal_boundary.left, self._shoal_boundary.right),
            random.uniform(self._shoal_boundary.top, self._shoal_boundary.bottom)
        )

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