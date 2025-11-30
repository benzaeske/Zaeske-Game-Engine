from pygame import Vector2, Rect


class SchoolParameters:

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
