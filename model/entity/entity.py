from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from pygame import Vector2

from model.world.modelcontext import ModelContext


class Entity(ABC):
    """
    Base class for all entities. Entities maintain a position and know how to draw themselves on screen.
    """
    def __init__(self, manager_id: UUID) -> None:
        self._id: UUID = uuid4()
        self.manager_id: UUID = manager_id
        self._position: Vector2 = Vector2(0,0)

    @abstractmethod
    def frame_actions(self, context: ModelContext, dt: float) -> None:
        """
        Actions that an entity takes each frame. May alter the state of this entity, other entity, the player, or
        the world state.
        :param context: A ModelContext representing the current state of the world model
        :param dt: The time delta between frames
        """
        pass

    @abstractmethod
    def move(self, context: ModelContext, dt: float) -> None:
        """
        Moves this entity
        :param context: A ModelContext representing the current state of the world model
        :param dt: The time delta between frames
        """
        pass

    def get_id(self) -> UUID:
        return self._id

    def get_manager_id(self) -> UUID:
        return self.manager_id

    def get_position(self) -> Vector2:
        return self._position

    def set_position(self, p: Vector2) -> None:
        self._position = p

    def get_x(self) -> float:
        return self._position.x

    def set_x(self, x: float) -> None:
        self._position.x = x

    def get_y(self) -> float:
        return self._position.y

    def set_y(self, y: float) -> None:
        self._position.y = y

    # Implement functions needed to make entity usable in a python set

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return NotImplemented
        return self._id == other.get_id()

    def __hash__(self):
        return hash(self._id)