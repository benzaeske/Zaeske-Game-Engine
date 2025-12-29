class WorldSpecs:
    def __init__(self, world_width: float, world_height: float, cell_size: float):
        self.world_width = world_width
        self.world_width_adj: float = self.world_width / 2
        self.world_height = world_height
        self.world_height_adj: float = self.world_height / 2
        self.cell_size = cell_size
        self.grid_width: int = int(self.world_width / self.cell_size)
        self.grid_height: int = int(self.world_height / self.cell_size)
