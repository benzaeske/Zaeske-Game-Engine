import copy
import uuid
from typing import Callable
from uuid import UUID
from abc import ABC, abstractmethod

from pygame import Vector2

from model.entities.gameentity import GameEntity
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class EntityGroupV1[T: GameEntity](ABC):
    """
    A group of entities of the same type that are controlled by the game.
    """
    def __init__(self):
        self.group_id: UUID = uuid.uuid4()
        self._entities: set[T] = set()

    @abstractmethod
    def update_entities(
        self,
        grid_space: GridSpace,
        get_group_ids_by_type: Callable[[EntityManagerIndex], set[UUID]],
        world_specs: WorldSpecs,
        player_position: Vector2 | None = None,
    ) -> None:
        """
        Updates all entities in their current position for a given frame by calculating forces applied to them. Does not update entity position since all
        forces need to be calculated for all entities before any of them move.
        :param grid_space: The current grid space
        :param get_group_ids_by_type: A function that takes an entity group type and returns a set of group ids for that type
        :param world_specs: Information about the world space
        :param player_position: The current position of the player
        """
        pass

    def move_entities(
        self,
        grid_space: GridSpace,
        world_specs: WorldSpecs,
        dt: float,
    ) -> None:
        """
        Moves all entities in the group based on delta time (dt) since the last frame.
        World width and world height are used for x-axis wrapping rules and preventing entities from leaving y-axis edge boundaries respectively.
        Updates the grid space if an entity changes which grid cell it is in after moving.
        """
        for entity in self._entities:
            old_position: Vector2 = copy.deepcopy(entity.position)
            entity.update_position(
                world_specs.world_width, world_specs.world_height, dt
            )
            grid_space.process_moved_entity_v1(old_position, entity)


    @abstractmethod
    def create_entity(self) -> T:
        """
        Factory method to create a new entity that belongs to this group.
        Tracks the created entity in this group's list of entities.
        """
        pass

    def add_entity(self, entity: T) -> None:
        self._entities.add(entity)

    def remove_entity(self, entity: T) -> None:
        self._entities.remove(entity)
