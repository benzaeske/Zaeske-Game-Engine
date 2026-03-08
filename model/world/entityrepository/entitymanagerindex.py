from enum import Enum


class EntityManagerIndex(Enum):
    """
    Indexes that can be used to quickly query for all entity manager ids based on a type of entity
    """
    RED_FISH = 0,
    YELLOW_FISH = 1,
    GREEN_FISH = 2,
    JELLY = 3,
    ENEMY = 4