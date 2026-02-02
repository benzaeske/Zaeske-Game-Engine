import uuid
from uuid import UUID
from abc import ABC, abstractmethod

from pygame import Vector2

from model.entities.gameentity import GameEntity
from model.player.cameraspecs import CameraSpecs
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class EntityGroup[T: GameEntity](ABC):
    def __init__(self):
        self.group_id: UUID = uuid.uuid4()
        self._entities: set[T] = set()

    @abstractmethod
    def update_entities(
        self,
        grid_space: GridSpace,
        entity_groups: dict[UUID, EntityGroup],
        world_specs: WorldSpecs,
        player_position: Vector2 | None = None,
    ) -> None:
        """
        Updates all entities in their current position for a given frame by calculating forces applied to them. Does not update entity position since all
        forces need to be calculated for all entities before any of them move.
        :param grid_space: The current grid space - Updating entities needs to be able to ask questions about what other entities are around them
        :param entity_groups: Updating entities needs to be able to ask questions about the parameters of other groups around them
        :param world_specs: Updating entities currently needs information about the size of the world for wrapping logic
        :param player_position: Provided in case entities need to behave based on their position relative to the player
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
            old_position: Vector2 = entity.position
            entity.update_position(
                world_specs.world_width, world_specs.world_height, dt
            )
            grid_space.process_moved_entity(old_position, entity)

    @abstractmethod
    def create_entity(
        self,
        world_specs: WorldSpecs,
        camera_specs: CameraSpecs | None = None,
        camera_position: Vector2 | None = None,
    ) -> T:
        """
        Factory method to create a new entity that belongs to this group.
        """
        pass

    def add_entity(self, entity: T) -> None:
        self._entities.add(entity)

    def remove_entity(self, entity: T) -> None:
        self._entities.remove(entity)
