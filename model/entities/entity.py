from abc import ABC, abstractmethod
from typing import Tuple, Callable
from uuid import UUID, uuid4

from pygame import Vector2, Surface, Rect

from model.player.player import Player
from model.world.entitygroupindex import EntityGroupIndex
from model.world.worldspecs import WorldSpecs


class Entity(ABC):
    """
    Base class for all entities
    """
    def __init__(self, sprite: Surface, group_id: UUID) -> None:
        self._id: UUID = uuid4()
        self.group_id: UUID = group_id
        self._position: Vector2 = Vector2(0,0)
        self._sprite: Surface = sprite
        self._sprite_w_adj: float = sprite.get_width() / 2
        self._sprite_h_adj: float = sprite.get_height() / 2

    @abstractmethod
    def frame_actions(self, context: FrameActionContext, dt: float) -> None:
        """
        Actions that this entity performs each frame. This could be changes to its own internal state, changes to other
        entities, changes to the world, or changes to the player.
        """
        pass

    @abstractmethod
    def move(self, context: EntityMovementContext, dt: float) -> None:
        """
        Moves this entity scaled by dt of this frame. This is intentionally separate from frame actions.
        All entities need to act in-place according to the world state at the start of the frame before anything moves.
        """
        pass

    def draw(self, screen: Surface, camera: Rect) -> None:
        """
        Draws the entity on the pygame screen
        :param screen: The screen to blit the entity on
        :param camera: The current size and position of the camera relative to the world space
        """
        screen.blit(self._sprite, self.to_camera_pos(camera))

    def to_camera_pos(self, camera: Rect) -> Tuple[float, float]:
        """
        Converts the entity's position in the model to the position it has on the pygame screen
        :param camera: The pygame Rect object representing the size and position of the camera relative to the world
        space
        :return: A tuple representing the top left corner of the entity on the pygame screen
        """
        return (
            self._position.x - camera.left - self._sprite_w_adj,
            # Note: The 'bottom' attribute of a pygame rect is actually the top edge since they are drawn top down
            camera.bottom - self._position.y - self._sprite_h_adj,
        )

    def get_id(self) -> UUID:
        return self._id

    def get_group_id(self) -> UUID:
        return self.group_id

    def get_position(self) -> Vector2:
        return self._position

    def set_position(self, p: Vector2) -> None:
        self._position = p

    def get_x(self) -> float:
        return self._position.x

    def get_y(self) -> float:
        return self._position.y

    # Implement functions needed to make entities usable in a python set

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return NotImplemented
        return self._id == other.get_id()

    def __hash__(self):
        return hash(self._id)

class FrameActionContext:
    """
    All information needed for performing frame actions. Provides restricted access into the underlying game model
    through callback functions.
    """
    def __init__(
            self,
            grid_space_access: GridSpaceEntityAccess,
            group_id_query_callback: Callable[[EntityGroupIndex], set[UUID]],
            world_specs: WorldSpecs,
            player: Player
    ) -> None:
        self.grid_space_access: GridSpaceEntityAccess = grid_space_access
        self.group_id_query_callback: Callable[[EntityGroupIndex], set[UUID]] = group_id_query_callback
        self.world_specs: WorldSpecs = world_specs
        self.player: Player = player

class GridSpaceEntityAccess:
    """
    Defines a set of functionality from the GridSpace that entities and entity groups are allowed to use during their
    update methods.
    """
    def __init__(
            self,
            add_entity: Callable[[Entity, Tuple[int, int] | None], None],
            process_moved_entity: Callable[[Vector2, Entity], None],
            get_entity_neighbors: Callable[[Entity, int, set[UUID]], list[Entity]]
    ) -> None:
        self.add_entity: Callable[[Entity, Tuple[int, int] | None], None] = add_entity
        self.process_moved_entity: Callable[[Vector2, Entity], None] = process_moved_entity
        self.get_entity_neighbors: Callable[[Entity, int, set[UUID]], list[Entity]] = get_entity_neighbors


class EntityMovementContext:
    """
    All Information needed for entities to perform movement
    """
    def __init__(self, world_specs: WorldSpecs):
        self.world_specs = world_specs


