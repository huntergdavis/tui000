import shutil
import sys
import asyncio

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static
from textual.events import Key

from package.headshot import Headshot  # Updated to use the Headshot widget
from package.lifemap import LifeMap    # Updated to use the LifeMap widget
from package.progressbar import ProgressBar
from package.eventlog import EventLog
from package.questionbox import QuestionBox
from package.bio import Bio
from package.lifequestions import LifeEventQuestions


class Tui000(App):

    CSS = """
    Screen {
        layout: vertical;
    }

    #top_container {
        height: auto;
    }

    #middle_container {
        height: auto;
    }

    #bottom_container {
        height: auto;
    }

    #left_container {
        width: 19;
    }

    #right_container {
        width: 20;
    }

    #debug_widget {
        width: 100%;
        height: 1;
    }

    #menu {
        height: 1;
    }

    #progress_bar {
        height: 3;
    }

    #event_log {
        height: 5;
    }

    #question_box {
        height: 14;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize variables
        self.debug_open = False
        self.life_map = [['X' for _ in range(60)] for _ in range(50)]
        self.question_box = QuestionBox(id="question_box")
        self.progress_bar = ProgressBar(id="progress_bar")
        self.event_log = EventLog(id="event_log")
        self.debug_widget = Static("", id="debug_widget")

        # Generate bio data using static methods
        self.character_name = Bio.generate_name()
        self.profession = Bio.generate_profession()
        self.age = Bio.generate_age()
        self.life_focus = Bio.generate_life_focus()

        # Create widgets that depend on generated data
        self.headshot_widget = Headshot(
            name=self.character_name,
            profession=self.profession,
            age=self.age,
            focus=self.life_focus,
            id="headshot_widget"
        )

        # Create life map widget
        self.life_map_widget = LifeMap(life_map_data=self.life_map, id="life_map_widget")

        # Create menu
        menu_content = "([b]G[/b]raveyard) ([b]O[/b]ptions) ([b]Q[/b]uit)"
        self.menu = Static(menu_content, id="menu")

    def compose(self) -> ComposeResult:
        # Top container with debug widget
        with Vertical(id="top_container"):
            yield self.debug_widget
            # Middle container with headshot, question box, and life map
            with Horizontal(id="middle_container"):
                # Left container with headshot
                with Vertical(id="left_container"):
                    yield self.headshot_widget
                # Center container with question box
                with Vertical():
                    yield self.question_box
                    yield self.event_log
                    yield self.progress_bar
                    yield self.menu
                # Right container with life map
                with Vertical(id="right_container"):
                    yield self.life_map_widget

    async def on_mount(self) -> None:
        # Perform any additional setup here
        await self.refreshQuestions()
        self.set_interval(10, self.refreshQuestions)  # Schedule refresh every 10 seconds
        self.event_log.add_entry("App started.")
        self.event_log.add_entry("Waiting for user input...")
        # Start the progress bar
        await self.progress_bar.start()

    async def refreshQuestions(self):
        questionandanswers = LifeEventQuestions.get_random_question()
        self.question = questionandanswers['question']
        self.choices = questionandanswers['choices']
        await self.question_box.display_question(self.question, self.choices)

    async def action_debug(self) -> None:
        if not self.debug_open:
            # Show the debug information
            terminal_size = shutil.get_terminal_size((80, 24))
            width, height = terminal_size.columns, terminal_size.lines
            debug_content = f"Terminal size: {width}x{height}"
            self.debug_widget.update(debug_content)
            self.debug_open = True
        else:
            # Hide the debug view
            self.debug_widget.update("")  # Clear the content
            self.debug_open = False

    async def on_key(self, event: Key) -> None:
        await self.question_box.on_key(event)  # Assuming this is async

        # Add new log entry for each key pressed
        self.event_log.add_entry(f"Key '{event.key}' pressed.")
        self.event_log.scroll_down()

        # Exit the program when 'q' is pressed
        if event.key.lower() == "q":
            self.exit()  # Use Textual's built-in exit method
        # Show or hide the debug screen after pressing the options 'o' key
        elif event.key.lower() == "o":
            await self.action_debug()

            # Refresh the question box with a new question
            await self.refreshQuestions()

        # Scroll up or down using arrow keys
        if event.key == "up":
            for _ in range(5):
                self.event_log.scroll_up()
        elif event.key == "down":
            for _ in range(5):
                self.event_log.scroll_down()

    async def on_ready(self) -> None:
        print("App is ready. Press 'q' to quit.")


if __name__ == "__main__":
    try:
        # Only have a log file if -log is passed in
        # Otherwise, don't log at all
        app = Tui000()
        if len(sys.argv) > 1 and sys.argv[1] == "-log":
            app.run(log="textual.log")
        else:
            app.run()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
    except asyncio.CancelledError:
        print("The application was cancelled.", file=sys.stderr)
