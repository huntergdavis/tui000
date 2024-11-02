from textual.widget import Widget
from rich.text import Text
from statistics import mode, StatisticsError
import random

class LifeMap(Widget):
    blocks_per_row: int = 10
    total_rows: int = 24
    colors = [
        "red", "green", "yellow", "blue", "magenta", "cyan", "white",
        "bright_red", "bright_green", "bright_yellow", "bright_blue",
        "bright_magenta", "bright_cyan"
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize life map data as an instance variable
        self.life_map = [['X' for _ in range(60)] for _ in range(50)]
        # Initialize a color map to store assigned colors for each block
        self.color_map = {}

    def update_life_map(self, new_data):
        """Method to update the life map data."""
        self.life_map = new_data
        self.refresh()  # Refresh the widget to reflect changes

    def render(self) -> Text:
        life_map_text = Text()
        blocks_per_row = self.blocks_per_row
        total_rows = self.total_rows

        for i in range(total_rows):
            for j in range(blocks_per_row):
                block_content = []
                start_row = (i * 50) // total_rows
                end_row = ((i + 1) * 50) // total_rows
                start_col = (j * 60) // blocks_per_row
                end_col = ((j + 1) * 60) // blocks_per_row

                for row in range(start_row, end_row):
                    for col in range(start_col, end_col):
                        block_content.append(self.life_map[row][col])

                try:
                    most_common = mode(block_content)
                except StatisticsError:
                    most_common = 'X'

                # Assign a consistent color based on the block position
                block_key = (i, j)
                if block_key not in self.color_map:
                    self.color_map[block_key] = random.choice(self.colors)
                color = self.color_map[block_key]

                life_map_text.append(most_common + " ", style=color)
            life_map_text.append("\n")

        return life_map_text
