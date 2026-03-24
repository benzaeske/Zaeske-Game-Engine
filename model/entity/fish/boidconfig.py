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
    ) -> None:
        """
        :param cohere_distance: The distance at which boids in this group will attempt to come together.
            Needs to be less than or equal to interaction_cell_range * grid cell size for the algorithm to work properly
        :param avoid_distance: The distance at which boids in this group will avoid each other.
            Should be smaller than cohere_distance
        :param interaction_cell_range: The range of grid cells around which to check for neighbors. Needs to be large
            enough to encompass cohere and avoid distance.
        :param cohere_k: How strongly boids in the group will attempt to cohere with neighbors in their coherence radius
        :param avoid_k: How strongly boids in the group will avoid neighbors in their avoid radius
        :param align_k: How strongly boids in the group will attempt to align their velocity
        """
        self.cohere_distance: float = cohere_distance
        self.avoid_distance: float = avoid_distance
        self.interaction_cell_range: int = interaction_cell_range
        self.cohere_k: float = cohere_k
        self.avoid_k: float = avoid_k
        self.align_k: float = align_k