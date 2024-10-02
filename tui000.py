import shutil
import sys
from textual.app import App
from textual.widgets import Static
from textual.events import Key
import asyncio
from statistics import mode

class Tui000(App):
    
    # Static variable for if options screen is open
    debug_open = False

    # Static variable to reference the options screen
    debug = None

    # current character name
    name = "Toast"
    profession = "Executive"
    age = 18
    life_focus = "Survival"

    # structure to hold 50 weekends per year and 60 years of life after 18
    # initialize all values to single character 'X" to represent unvisited
    # structure is a 2D array of 50x60
    life_map = [['X' for i in range(60)] for j in range(50)]

    # Function for generating the life_map string based on the character's life_map
    # Each character represents a block of weekends, displayed in a 12x10 grid with padding.
    def generate_life_map(self) -> str:
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
                        weekends_block.append(self.life_map[row][col])

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


    # Function for generating the headshot in the corner (9x9 box)
    def generate_headshot(self) -> str:
        return "\n".join([
            "  .   .  ",
            "   \\ /   ",
            "    X    ",
            "   / \\   ",
            "  '   '  ",
        ])

    async def on_mount(self) -> None:
        # Get the terminal size
        terminal_size = shutil.get_terminal_size((80, 24))
        width, height = terminal_size.columns, terminal_size.lines

        # Check if terminal is at least 80x24
        if width < 80 or height < 24:
            print("Terminal size must be at least 80x24. Exiting.", file=sys.stderr)
            await asyncio.sleep(1)  # Wait for one second before exiting
            sys.exit(1)

        # Create the 9x9 square box with the headshot
        box = Static(self.generate_headshot())

        # Create the life_map on the upper right side of the screen
        life_map = Static(self.generate_life_map())

        # Dock the headshot on the left, taking up 10 columns and 10 rows
        await self.view.dock(box, edge="left", size=10)

        # Dock the life_map on the top-right (22 characters wide, 12 rows tall)
        await self.view.dock(life_map, edge="right", size=20)  # 22 chars wide

        # Create the menu row with highlighted letters
        menu_content = "([b]S[/b]ave) ([b]L[/b]oad) ([b]G[/b]raveyard) ([b]O[/b]ptions) ([b]Q[/b]uit)"
        menu = Static(menu_content)

        # Add the menu to the bottom
        await self.view.dock(menu, edge="bottom", size=1)

        # Initialize the debug screen as a Static widget
        Tui000.debug = Static("")  # Start with empty content
        await self.view.dock(Tui000.debug, edge="top", size=1)  # Dock it at the top


    # Function for when the options key is pressed
    async def action_debug(self) -> None:
        if not Tui000.debug_open:
            # Show the debug information
            terminal_size = shutil.get_terminal_size((80, 24))
            width, height = terminal_size.columns, terminal_size.lines
            debug_content = f"Terminal size: {width}x{height}"
            await Tui000.debug.update(debug_content)  # Update the existing debug widget
            Tui000.debug_open = True
        else:
            # Hide the debug view
            await Tui000.debug.update("")  # Clear the content
            Tui000.debug_open = False

    async def on_key(self, event: Key) -> None:
        # Exit the program when 'q' is pressed
        if event.key.lower() == "q":  # Check for lowercase 'q'
            await self.action_quit()  # Use Textual's built-in quit action
        # Show or hide the debug screen after pressing the options 'o' key
        elif event.key.lower() == "o":
            await self.action_debug()

    async def on_ready(self) -> None:
        print("App is ready. Press 'q' to quit.")

if __name__ == "__main__":
    try:
        Tui000.run(log="textual.log")
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
    except asyncio.CancelledError:
        print("The application was cancelled.", file=sys.stderr)
