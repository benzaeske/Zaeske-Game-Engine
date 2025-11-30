from pygame import Vector2, Rect


class SchoolParameters:
    """
    Defines schooling behavior for a school of fish
    :param cohere_distance: The distance at which fish in the school will attempt to come together. Needs to be less than or equal to interaction_cell_range * grid cell size for the algorithm to work properly
    :param avoid_distance: The distance at which fish in the school will avoid each other. Should be smaller than cohere_distance
    :param interaction_cell_range: The range of grid cells around which to check for neighbors when performing boids algorithm
    :param cohere_k: How strongly fish in the school will attempt to cohere with neighbors in their coherence radius
    :param avoid_k: How strongly fish in the school will avoid neighbors in their avoid radius
    :param align_k: How strongly fish in the school will attempt to align their velocities
    :param shoal_location: A location that fish will 'shoal' to. They will target the shoal location when far from it, and swim 'around' it when near
    :param shoal_radius: The radius of the shoal - determines when fish in the school will go towards the shoal vs swim 'around' it
    :param shoal_k: How strongly fish in the school will prioritize movement about the shoal location
    :param hatch_region: A rectangle that defines the region in which this school of fish can spawn
    :param egg_count: The number of fish this school can support
    """

    def __init__(
        self,
        cohere_distance: float,
        avoid_distance: float,
        interaction_cell_range: int,
        cohere_k: float,
        avoid_k: float,
        align_k: float,
        shoal_location: Vector2 | None,
        shoal_radius: float,
        shoal_k: float,
        hatch_region: Rect,
        egg_count: int,
    ) -> None:
        self.cohere_distance: float = cohere_distance
        self.avoid_distance: float = avoid_distance
        self.interaction_cell_range: int = interaction_cell_range
        self.cohere_k: float = cohere_k
        self.avoid_k: float = avoid_k
        self.align_k: float = align_k
        self.shoal_location: Vector2 = shoal_location
        self.shoal_radius: float = shoal_radius
        self.shoal_k: float = shoal_k
        self.hatch_region: Rect = hatch_region
        self.egg_count: int = egg_count
