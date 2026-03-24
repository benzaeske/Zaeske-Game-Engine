from enum import StrEnum


class PlayerAnimation(StrEnum):
    """
    Enumerates all possible animations for the player
    """
    IDLE_LEFT = "IDLE_LEFT"
    IDLE_RIGHT = "IDLE_RIGHT"
    SWIMMING_LEFT = "SWIMMING_LEFT"
    SWIMMING_RIGHT = "SWIMMING_RIGHT"