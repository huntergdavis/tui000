import shutil
import sys
import asyncio

from textual.app import App
from textual.widgets import Static
from textual.events import Key

from package.headshot import generate_headshot
from package.lifemap import generate_life_map

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
        box = Static(generate_headshot())

        # Create the life_map on the upper right side of the screen
        life_map = Static(generate_life_map(life_map=self.life_map))

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
