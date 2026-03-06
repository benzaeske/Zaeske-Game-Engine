import uuid
from abc import ABC, abstractmethod
from uuid import UUID

from pygame import Vector2

from model.player.cameraspecs import CameraSpecs
from model.player.player import Player
from model.world.entitymanagerindex import EntityManagerIndex
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class EntityManager(ABC):
    """
    Facilitates frame actions and movement for one or many entities. Takes information from the underlying data
    structures in the model and passes along necessary information to individual entities.
    """
    def __init__(self):
        self._manager_id: UUID = uuid.uuid4()

    @abstractmethod
    def frame_actions(self, context: ModelContext, dt: float) -> None:
        """
        Actions to perform each frame. Actions can alter the state of the contained entities within this manager, other
        entities in the world space, or the player. This is intentionally separated from movement. Each entity needs to
        perform its actions in-place before movement can be done.
        """

    @abstractmethod
    def movement(self, context: ModelContext, dt: float) -> None:
        """
        Performs any necessary movement of tracked entities. This is intentionally separated from frame_actions. Each
        entity needs to perform its actions in-place before movement can be done.
        """

    def get_manager_id(self) -> UUID:
        return self._manager_id

class ModelContext:
    """
    Wrapper around data structures stored in the model that entity managers may need for their frame actions or movement
    methods. Provides helper functions for quick access of certain methods and data.
    """
    def __init__(
            self,
            grid_space: GridSpace,
            entity_manager_indexes: dict[EntityManagerIndex, set[UUID]],
            player: Player,
            world_specs: WorldSpecs,
    ) -> None:
        self.grid_space: GridSpace = grid_space
        self.entity_manager_indexes: dict[EntityManagerIndex, set[UUID]] = entity_manager_indexes
        self.player: Player = player
        self.world_specs: WorldSpecs = world_specs

    def get_manager_ids_by_type(self, index: EntityManagerIndex) -> set[UUID]:
        return self.entity_manager_indexes.get(index, set())

    def get_world_width(self) -> float:
        return self.world_specs.world_width

    def get_world_height(self) -> float:
        return self.world_specs.world_height

    def get_player_position(self) -> Vector2:
        return self.player.position

    def get_camera_position(self) -> Vector2:
        return Vector2(self.player.camera.center)

    def get_camera_specs(self) -> CameraSpecs:
        return self.player.camera_specs