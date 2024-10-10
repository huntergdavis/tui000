import shutil
import sys
import asyncio

from textual.app import App
from textual.widgets import Static
from textual.events import Key
from textual.reactive import Reactive

from rich.text import Text

from package.headshot import generate_headshot
from package.lifemap import life_map_display
from package.progressbar import ProgressBar
from package.eventlog import EventLog

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
        # Create the 9x9 square box with the headshot
        box = Static(generate_headshot())
        await self.view.dock(box, edge="left", size=10)

        # Create the life_map on the upper right side of the screen
        life_map = Static(life_map_display(life_map=self.life_map))
        await self.view.dock(life_map, edge="right", size=20)  # Adjusted size for better fit

        # Create the menu row and dock it at the bottom
        menu_content = "([b]S[/b]ave) ([b]L[/b]oad) ([b]G[/b]raveyard) ([b]O[/b]ptions) ([b]Q[/b]uit)"
        menu = Static(menu_content)
        await self.view.dock(menu, edge="bottom", size=1)

        # Create the progress bar widget and dock it just above the menu
        self.progress_bar = ProgressBar(percentage=100)
        await self.view.dock(self.progress_bar, edge="bottom", size=3)

        # Create the event log widget and dock it in the bottom space
        self.event_log = EventLog()
        await self.view.dock(self.event_log, edge="bottom", size=5)  # Height of 5 lines

        # Initialize the debug screen as a Static widget
        Tui000.debug = Static("")  # Start with empty content
        await self.view.dock(Tui000.debug, edge="top", size=1)

        # Add some initial log entries
        await self.event_log.add_entry("App started.")
        await self.event_log.add_entry("Waiting for user input...")


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
        # Add new log entry for each key pressed
        await self.event_log.add_entry(f"Key '{event.key}' pressed.")

        # Exit the program when 'q' is pressed
        if event.key.lower() == "q":  # Check for lowercase 'q'
            await self.action_quit()  # Use Textual's built-in quit action
        # Show or hide the debug screen after pressing the options 'o' key
        elif event.key.lower() == "o":
            await self.action_debug()

        # Scroll up or down using arrow keys
        if event.key == "up":
            await self.event_log.scroll_up()
        elif event.key == "down":
            await self.event_log.scroll_down()

    async def on_ready(self) -> None:
        print("App is ready. Press 'q' to quit.")

if __name__ == "__main__":
    try:
        # only have a log file if -log is passed in 
        # otherwise, don't log at all 
        if len(sys.argv) > 1 and sys.argv[1] == "-log":
            Tui000.run(log="textual.log")
        else:
            Tui000.run()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
    except asyncio.CancelledError:
        print("The application was cancelled.", file=sys.stderr)
