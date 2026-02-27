import copy
import uuid
from abc import ABC, abstractmethod
from typing import Callable
from uuid import UUID

from pygame import Vector2

from model.player.player import Player
from model.world.entitygroupindex import EntityGroupIndex
from model.world.gridspace import GridSpace


class PlayerEntity(ABC):
    """
    An entity that belongs to the player in some way.
    """
    def __init__(self, initial_pos: Vector2):
        self.entity_id: uuid.UUID = uuid.uuid4()
        self.position: Vector2 = copy.deepcopy(initial_pos)

    @abstractmethod
    def update(self, grid_space: GridSpace, get_group_ids_by_type: Callable[[EntityGroupIndex], set[UUID]], player: Player, dt: float) -> None:
        """
        :param grid_space: Player entities can query and interact with the grid space, but are not stored in the grid space themselves.
        :param get_group_ids_by_type: Player entities need to be able to get a set of entity ids by type
        :param player: Player entities have full read/write access to the player during their update method
        :param dt: Player entities may need delta time for movement calculations
        """
        pass