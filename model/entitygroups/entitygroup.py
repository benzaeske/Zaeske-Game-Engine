import uuid
from abc import ABC, abstractmethod

from pygame import Vector2

from model.entities.gameentity import GameEntity
from model.player.cameraspecs import CameraSpecs
from model.world.grid_cell import GridCell
from model.world.worldspecs import WorldSpecs


class EntityGroup[T: GameEntity](ABC):
    def __init__(self):
        self.group_id: uuid.UUID = uuid.uuid4()
        self.entities: dict[uuid.UUID, T] = {}

    @abstractmethod
    def update_entities(
        self,
        world_specs: WorldSpecs,
        #TODO GridSpace class instead of 2d array
        grid_space: list[list[GridCell]],
        entity_groups: dict[uuid.UUID, EntityGroup],
        player_position: Vector2 | None = None,
    ) -> None:
        """
        Updates all entities in their current position for a given frame. Does not move them.
        """
        pass

    def move_entities(
        self,
        world_specs: WorldSpecs,
        # TODO GridSpace class instead of 2d array
        grid_space: list[list[GridCell]],
        dt: float,
    ) -> None:
        """
        Moves all entities in the group based on delta time (dt) since the last frame.
        World width and world height are used for x-axis wrapping rules and preventing entities from leaving y-axis edge boundaries respectively.
        Updates individual grid cells if the entity changes the grid cell it is in after processing the position update.
        """
        for entity in self.entities.values():
            old_r = int(entity.position.y / world_specs.cell_size)
            old_c = int(entity.position.x / world_specs.cell_size)
            entity.update_position(
                world_specs.world_width, world_specs.world_height, dt
            )
            # Check if we are in a new grid cell after moving
            new_r = int(entity.position.y / world_specs.cell_size)
            new_c = int(entity.position.x / world_specs.cell_size)
            if new_r != old_r or new_c != old_c:
                grid_space[old_r][old_c].remove_entity(entity)
                grid_space[new_r][new_c].add_entity(entity)

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
        self.entities[entity.entity_id] = entity

    def remove_entity(self, entity: T) -> None:
        self.entities.pop(entity.entity_id)
