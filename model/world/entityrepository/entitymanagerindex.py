from enum import StrEnum


class EntityManagerIndex(StrEnum):
    """
    Indexes that can be used to quickly query for all entity manager ids based on a type of entity
    """
    FISH = "FISH"
    RED_FISH = "RED_FISH",
    YELLOW_FISH = "YELLOW_FISH",
    GREEN_FISH = "GREEN_FISH",
    ENEMY = "ENEMY",
    ITEM = "ITEM"