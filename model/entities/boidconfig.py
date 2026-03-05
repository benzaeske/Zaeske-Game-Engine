from pygame import Vector2


class BoidConfig:
    """
    Base properties needed for performing Boids algorithm
    """
    def __init__(
        self,
        cohere_distance: float,
        avoid_distance: float,
        interaction_cell_range: int,
        cohere_k: float,
        avoid_k: float,
        align_k: float,
        target_location: Vector2 | None,
        target_radius: float,
        target_k: float,
    ) -> None:
        """
        :param cohere_distance: The distance at which boids in this group will attempt to come together.
            Needs to be less than or equal to interaction_cell_range * grid cell size for the algorithm to work properly
        :param avoid_distance: The distance at which boids in this group will avoid each other.
            Should be smaller than cohere_distance
        :param interaction_cell_range: The range of grid cells around which to check for neighbors
        :param cohere_k: How strongly boids in the group will attempt to cohere with neighbors in their coherence radius
        :param avoid_k: How strongly boids in the group will avoid neighbors in their avoid radius
        :param align_k: How strongly boids in the group will attempt to align their velocity
        :param target_location: An optional location that boids in this group will target.
            They will target the location when far from it, and move 'around' it when near
        :param target_radius: The radius of the target location.
            Determines when boids in the group will go towards the location vs move 'around' it.
        :param target_k: How strongly boids in the group will prioritize movement about the target.
        """
        self.cohere_distance = cohere_distance
        self.avoid_distance = avoid_distance
        self.interaction_cell_range = interaction_cell_range
        self.cohere_k = cohere_k
        self.avoid_k = avoid_k
        self.align_k = align_k
        self.target_location = target_location
        self.target_radius = target_radius
        self.target_k = target_k