class WorldSpecs:
    def __init__(self, cell_size: float, grid_width: int, grid_height: int) -> None:
        self.cell_size: float = cell_size
        self.grid_width: int = grid_width
        self.grid_height: int = grid_height
        self.world_width: float = self.grid_width * self.cell_size
        self.world_width_adj: float = self.world_width / 2
        self.world_height: float = self.grid_height * self.cell_size
        self.world_height_adj: float = self.world_height / 2
