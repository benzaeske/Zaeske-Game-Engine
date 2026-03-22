from enum import Enum


class EntityManagerIndex(Enum):
    """
    Indexes that can be used to quickly query for all entity manager ids based on a type of entity
    """
    FISH = 0
    RED_FISH = 1,
    YELLOW_FISH = 2,
    GREEN_FISH = 3,
    ENEMY = 4,
    ITEM = 5