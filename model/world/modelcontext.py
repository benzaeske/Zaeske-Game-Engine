from model.player.playerinterface import PlayerInterface
from model.world.entityrepository.entityrepositoryinterface import EntityRepositoryInterface
from model.world.gridspace.gridspaceinterface import GridSpaceInterface
from model.world.worldspecs import WorldSpecs


class ModelContext:
    """
    Provides controlled access into the current state of the world model.
    """
    def __init__(
            self,
            world_specs: WorldSpecs,
            grid_space: GridSpaceInterface,
            entity_repository: EntityRepositoryInterface,
            player: PlayerInterface
    ) -> None:
        self.world_specs: WorldSpecs = world_specs
        self.grid_space: GridSpaceInterface = grid_space
        self.entity_repository: EntityRepositoryInterface = entity_repository
        self.player: PlayerInterface = player

    def get_world_w(self) -> float:
        return self.world_specs.world_width

    def get_world_h(self) -> float:
        return self.world_specs.world_height

