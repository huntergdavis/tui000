from statistics import mode
import random
from rich.text import Text

def life_map_display(life_map) -> Text:
    life_map_text = Text()
    blocks_per_row = 10
    total_rows = 24
    colors = [
        "red", "green", "yellow", "blue", "magenta", "cyan", "white",
        "bright_red", "bright_green", "bright_yellow", "bright_blue",
        "bright_magenta", "bright_cyan"
    ]

    # Initialize a color map to store assigned colors for each block
    color_map = {}

    for i in range(total_rows):
        for j in range(blocks_per_row):
            weekends_block = []
            start_row = (i * 50) // total_rows
            end_row = ((i + 1) * 50) // total_rows
            start_col = (j * 60) // blocks_per_row
            end_col = ((j + 1) * 60) // blocks_per_row

            for row in range(start_row, end_row):
                for col in range(start_col, end_col):
                    weekends_block.append(life_map[row][col])

            most_common = mode(weekends_block)

            # Assign a consistent color based on the block position
            block_key = (i, j)
            if block_key not in color_map:
                color_map[block_key] = random.choice(colors)
            color = color_map[block_key]

            life_map_text.append(most_common + " ", style=color)
        life_map_text.append("\n")

    return life_map_text
