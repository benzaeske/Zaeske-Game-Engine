from enum import Enum


class EntityGroupIndex(Enum):
    """
    Indexes that can be used to quickly query the entity manager for a set of group ids
    If a value is added here, make sure to update the EntityManager.index_entity_group function appropriately
    """
    RED_FISH = 0,
    YELLOW_FISH = 1,
    GREEN_FISH = 2,
    JELLY = 3,
    ENEMY = 4