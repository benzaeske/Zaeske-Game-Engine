import math
from uuid import UUID

from pygame import Surface, Vector2, Rect, transform

from model.entities.boidconfig import BoidConfig
from model.entities.physicsentity import PhysicsEntity
from model.world.modelcontext import ModelContext


class Boid(PhysicsEntity):
    """
    Base implementation of agents that follow Boids algorithm. Uses position/velocity/acceleration to perform movement.
    """
    def __init__(
            self,
            sprite: Surface,
            manager_id: UUID,
            max_speed: float,
            max_acceleration: float,
            boid_config: BoidConfig,
    ) -> None:
        super().__init__(sprite, manager_id, max_speed, max_acceleration)
        self._boid_config: BoidConfig = boid_config

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        self.flock(context)
        self.flock_to_target()

    def flock(self, context: ModelContext) -> None:
        """
        Implementation of boids algorithm that follows the three rules of avoidance, alignment, and coherence.
        """
        sum_avoid: Vector2 = Vector2(0.0, 0.0)
        sum_align: Vector2 = Vector2(0.0, 0.0)
        sum_cohere: Vector2 = Vector2(0.0, 0.0)
        count_n: int = 0
        count_s: int = 0
        for neighbor in context.grid_space.get_neighbors_for_entity(self, self._boid_config.interaction_cell_range,
                                                                    None):
            if self.get_id() != neighbor.get_id():  # Make sure we don't check an entity against itself
                d: float = self.get_position().distance_to(neighbor.get_position())
                if 0 < d < self._boid_config.cohere_distance:
                    sum_align += neighbor.get_velocity()
                    sum_cohere += neighbor.get_position()
                    count_n += 1
                if 0 < d < self._boid_config.avoid_distance:
                    diff: Vector2 = self.get_position() - neighbor.get_position()
                    diff.normalize_ip()
                    diff /= d
                    sum_avoid += diff
                    count_s += 1
        if count_s > 0:
            self.target(sum_avoid, self._boid_config.avoid_k)
        if count_n > 0:
            self.target(sum_align, self._boid_config.align_k)
            sum_cohere /= float(count_n)
            sum_cohere -= self.get_position()
            self.target(sum_cohere, self._boid_config.cohere_k)

    def flock_to_target(self) -> None:
        """
        Boids in a group can optionally target a location in addition to flocking together. This is set by changing the
        BoidConfig.target_location
        """
        if self._boid_config.target_location is not None:
            d: float = self.get_position().distance_to(self._boid_config.target_location)
            diff = self._boid_config.target_location - self.get_position()
            if d > self._boid_config.target_radius:
                self.target(diff, self._boid_config.target_k)
            else:
                self.target(diff, -self._boid_config.target_k)

    def avoid_walls(self, context: ModelContext) -> None:
        """
        Rudimentary wall avoidance. Currently only avoids the floor and ceiling of the map... and not very well. Needs
        to be changed to use the PhysicsEntity.target function and work with any arbitrary walls defined in the grid
        space.
        """
        # TODO make this better
        avoid_edge_dist: float = 128.0
        if self.get_y() < avoid_edge_dist and self.get_velocity().y < 0:
            self.apply_acceleration(Vector2(0.0, self.get_max_speed() / 2))
        if self.get_y() > context.get_world_h() - avoid_edge_dist and self.get_velocity().y > 0:
            self.apply_acceleration(Vector2(0.0, -(self.get_max_speed() / 2)))

    def draw(self, screen: Surface, camera: Rect) -> None:
        # Rotate the boid according to its velocity then blit it to the screen
        rotated_surface: Surface = transform.rotate(self._sprite, math.degrees(math.atan2(self._velocity.y, self._velocity.x)))
        screen.blit(rotated_surface, self.to_camera_pos(camera))