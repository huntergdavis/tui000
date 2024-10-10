from statistics import mode

# Function for generating the life_map string based on the character's life_map
# Each character represents a block of weekends, displayed in a 12x10 grid with padding.
def life_map_display(life_map) -> str:
    # Initialize the life_map string
    life_map_str = ""

    # Each row in the grid will contain 10 blocks, displayed with spaces to fill 22 characters
    # We need to condense 50 rows x 60 columns into 12x10 blocks
    blocks_per_row = 10
    total_rows = 12

    # Each block represents ~25 weekends (25 = 50x60 / 120)
    for i in range(total_rows):  # 12 rows in the final grid
        row_str = ""
        for j in range(blocks_per_row):  # 10 blocks per row
            # For each block, we gather ~25 weekends
            weekends_block = []

            # Calculate the range of weekends for this block
            start_row = (i * 50) // total_rows  # scale row index down from 12 to 50
            end_row = ((i + 1) * 50) // total_rows

            start_col = (j * 60) // blocks_per_row  # scale col index down from 10 to 60
            end_col = ((j + 1) * 60) // blocks_per_row

            # Gather the weekends in the block
            for row in range(start_row, end_row):
                for col in range(start_col, end_col):
                    weekends_block.append(life_map[row][col])

            # Calculate the mode of the block (most frequent character)
            most_common = mode(weekends_block)

            # Add the mode character, with padding space around it for display
            row_str += most_common + " "  # Each block followed by a space

        # Add the formatted row to the life_map_str
        life_map_str += row_str.rstrip() + "\n"  # Remove trailing space, add newline

        # Add a blank line for padding between rows (except after the last row)
        #if i < total_rows - 1:
        #    life_map_str += "\n"  # Blank line for padding

    return life_map_str


