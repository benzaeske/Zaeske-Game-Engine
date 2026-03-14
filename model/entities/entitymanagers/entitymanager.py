import uuid
from abc import ABC, abstractmethod
from uuid import UUID

from model.world.modelcontext import ModelContext


class EntityManager(ABC):
    """
    Orchestrates frame actions and movement for one or many entities.
    """
    def __init__(self):
        self._manager_id: UUID = uuid.uuid4()

    @abstractmethod
    def frame_actions(self, context: ModelContext, dt: float) -> None:
        """
        Actions to perform each frame. Actions can alter the state of the contained entities within this manager, other
        entities in the world space, or the player.
        """

    @abstractmethod
    def movement(self, context: ModelContext, dt: float) -> None:
        """
        Performs any necessary movement of tracked entities.
        """

    def get_manager_id(self) -> UUID:
        return self._manager_id