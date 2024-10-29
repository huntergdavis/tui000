###############################################################################
# Jds-Tinkering2 (branch) version
# Last updated -- 2024-10-29
#
###############################################################################

import shutil
import sys
import asyncio

from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.reactive import Reactive
from textual.events import Key

from rich.text import Text

from package.headshot import generate_headshot_and_bio
from package.lifemap import life_map_display
from package.progressbar import ProgressBar
from package.eventlog import EventLog
from package.questionbox import QuestionBox
from package.bio import Bio
from package.lifequestions import LifeEventQuestions

class Tui000(App):
    # Static variable for if options screen is open
    debug_open = False

    # Static variable to reference the options screen
    debug = None

    # Reactive properties for character attributes
    name = Reactive("")
    profession = Reactive("")
    age = Reactive(0)
    life_focus = Reactive("")
    question = Reactive("")
    choices = Reactive([])  # Initialize as empty list

    # structure to hold 50 weekends per year and 60 years of life after 18
    # initialize all values to single character 'X" to represent unvisited
    # structure is a 2D array of 50x60
    life_map = [['X' for i in range(60)] for j in range(50)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debug = None
        
    async def refreshQuestions(self):
        questionandanswers = LifeEventQuestions.get_random_question()
        self.question = questionandanswers['question']
        self.choices = questionandanswers['choices']
        await self.question_box.display_question(self.question, self.choices)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        # Initialize widgets
        self.question_box = QuestionBox()
        self.event_log = EventLog()
        self.progress_bar = ProgressBar()
        self.debug = Static("", id="debug")       ##

        # Generate character info
        self.name = Bio.generate_name(self)
        self.profession = Bio.generate_profession(self)
        self.age = Bio.generate_age(self)
        self.life_focus = Bio.generate_life_focus(self)
        
        # Get initial question
        questionandanswers = LifeEventQuestions.get_random_question()
        self.question = questionandanswers['question']
        self.choices = questionandanswers['choices']

        # Create and yield widgets in the desired layout order
        yield Static(generate_headshot_and_bio(self.name, self.profession, self.age, self.life_focus), classes="headshot")
        yield Static(life_map_display(life_map=self.life_map), classes="lifemap")
        yield self.question_box
        yield self.event_log
        yield self.progress_bar
        yield Static("([b]G[/b]raveyard) ([b]O[/b]ptions) ([b]Q[/b]uit)", classes="menu")
        yield self.debug

    async def on_mount(self) -> None:
        # Initial setup
        await self.question_box.display_question(self.question, self.choices)
        await self.event_log.add_entry("App started.")
        await self.event_log.add_entry("Waiting for user input...")
        await self.progress_bar.start()

        # Set up question refresh interval
        self.set_interval(10, self.refreshQuestions)

    # Function for when the options key is pressed
    async def action_debug(self) -> None:
        if self.debug is None:
            await self.event_log.add_entry("Debug widget not initialized")
            return
    
        if not self.debug_open:
            terminal_size = shutil.get_terminal_size((80, 24))
            width, height = terminal_size.columns, terminal_size.lines
            debug_content = f"Terminal size: {width}x{height}"
            self.debug.update(debug_content)  # Remove await here
            self.debug_open = True
        else:
            self.debug.update("")  # Remove await here
            self.debug_open = False

    async def on_key(self, event: Key) -> None:
        # Handle key events for the question box
        await self.question_box.on_key(event)
        
        # Add new log entry for each key pressed
        await self.event_log.add_entry(f"Key '{event.key}' pressed.")
        await self.event_log.scroll_down()

        # Exit the program when 'q' is pressed
        if event.key.lower() == "q":
            await self.action_quit()

        # Show or hide the debug screen after pressing the options 'o' key
        elif event.key.lower() == "o":
            await self.action_debug()
            await self.refreshQuestions()

        # Scroll up or down using arrow keys
        if event.key == "up":
            for i in range(5):
                await self.event_log.scroll_up()
        elif event.key == "down":
            for i in range(5):
                await self.event_log.scroll_down()

    # Add CSS styles for layout
    CSS = """
    .headshot {
        dock: left;
        width: 19;
    }
    .lifemap {
        dock: right;
        width: 20;
    }
    QuestionBox {
        height: 14;
    }
    EventLog {
        height: 5;
    }
    ProgressBar {
        height: 3;
    }
    .menu {
        height: 1;
        dock: bottom;
    }
    """

if __name__ == "__main__":
    try:
        # only have a log file if -log is passed in 
        # otherwise, don't log at all 
        if len(sys.argv) > 1 and sys.argv[1] == "-log":
            app = Tui000()
            app.run(log="textual.log")
        else:
            app = Tui000()
            app.run()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
    except asyncio.CancelledError:
        print("The application was cancelled.", file=sys.stderr)
        