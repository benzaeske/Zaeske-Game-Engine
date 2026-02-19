from enum import Enum


class FishType(Enum):
    RED = 0
    GREEN = 1
    YELLOW = 2


class FishSettings:
    """
    Defines properties for an individual Fish entity
    :param fish_type: The type of fish to use. This determines which fish sprite gets loaded from the images directory
    :param width: The width of the fish in the model. The fish sprite will be initially scaled to this size
    :param height: The height of the fish in the model. The fish sprite will be initially scaled to this size
    :param max_speed: The maximum allowed magnitude of this Fish's velocity
    :param max_acceleration: The maximum magnitude of this Fish's acceleration per frame
    """

    def __init__(
        self,
        fish_type: FishType,
        width: float,
        height: float,
        max_speed: float,
        max_acceleration: float,
    ) -> None:
        self.fish_type: FishType = fish_type
        self.width: float = width
        self.height: float = height
        self.max_speed: float = max_speed
        self.max_acceleration: float = max_acceleration
