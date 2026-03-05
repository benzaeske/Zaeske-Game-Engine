import math
from uuid import UUID

from pygame import Surface, Vector2, Rect
from pygame.transform import rotate

from model.entities.boidconfig import BoidConfig
from model.entities.entity import Entity, FrameActionContext
from model.entities.physicsentity import PhysicsEntity
from model.utils.entityutils import calculate_shortest_distance_and_virtual_position


class Boid(PhysicsEntity):
    """
    Base implementation of agents that follow Boids algorithm. Uses position/velocity/acceleration to perform movement.
    """
    def __init__(
            self,
            sprite: Surface,
            group_id: UUID,
            max_speed: float,
            max_acceleration: float,
            config: BoidConfig
    ) -> None:
        super().__init__(sprite, group_id, max_speed, max_acceleration)
        self.config: BoidConfig = config

    def frame_actions(self, context: FrameActionContext, dt: float) -> None:
        neighbors: list[Entity] = context.grid_space_access.get_entity_neighbors(self, self.config.interaction_cell_range, set())
        self.flock(context, neighbors)
        self.flock_to_target(context)
        self.avoid_walls(context)

    def flock(self, context: FrameActionContext, neighbors: list[Entity]) -> None:
        """
        Implementation of boids algorithm that follows the three rules of avoidance, alignment, and coherence.
        """
        sum_avoid: Vector2 = Vector2(0.0, 0.0)
        sum_align: Vector2 = Vector2(0.0, 0.0)
        sum_cohere: Vector2 = Vector2(0.0, 0.0)
        count_n: int = 0
        count_s: int = 0
        for neighbor in neighbors:
            if self.get_id() != neighbor.get_id():  # Make sure we don't check an entity against itself
                d, other_pos = calculate_shortest_distance_and_virtual_position(
                    self.get_position(), neighbor.get_position(), context.world_specs.world_width
                )
                if 0 < d < self.config.cohere_distance:
                    sum_align += neighbor.get_velocity()
                    sum_cohere += other_pos
                    count_n += 1
                if 0 < d < self.config.avoid_distance:
                    diff: Vector2 = self.get_position() - other_pos
                    diff.normalize_ip()
                    diff /= d
                    sum_avoid += diff
                    count_s += 1
        if count_s > 0:
            self.target(sum_avoid, self.config.avoid_k)
        if count_n > 0:
            self.target(sum_align, self.config.align_k)
            sum_cohere /= float(count_n)
            sum_cohere -= self.get_position()
            self.target(sum_cohere, self.config.cohere_k)

    def flock_to_target(self, context: FrameActionContext) -> None:
        """
        Boids in a group can optionally target a location in addition to flocking together. This is set by changing the
        BoidConfig.target_location
        """
        if self.config.target_location is not None:
            d, shoal_pos = calculate_shortest_distance_and_virtual_position(
                self.get_position(), self.config.target_location, context.world_specs.world_width
            )
            diff = shoal_pos - self.get_position()
            if d > self.config.target_radius:
                self.target(diff, self.config.target_k)
            else:
                self.target(diff, -self.config.target_k)

    def avoid_walls(self, context: FrameActionContext) -> None:
        """
        Rudimentary wall avoidance. Currently only avoids the floor and ceiling of the map... and not very well. Needs
        to be changed to use the PhysicsEntity.target function and work with any arbitrary walls defined in the grid
        space.
        """
        # TODO make this better
        avoid_edge_dist: float = 128.0
        if self.get_y() < avoid_edge_dist and self.get_velocity().y < 0:
            self.apply_acceleration(Vector2(0.0, self.get_max_speed() / 2))
        if self.get_y() > context.world_specs.world_height - avoid_edge_dist and self.get_velocity().y > 0:
            self.apply_acceleration(Vector2(0.0, -(self.get_max_speed() / 2)))

    def draw(self, screen: Surface, camera: Rect) -> None:
        # Rotate the boid according to its velocity then blit it to the screen
        rotated_surface: Surface = rotate(self._sprite, math.degrees(math.atan2(self._velocity.y, self._velocity.x)))
        screen.blit(rotated_surface, self.to_camera_pos(camera))