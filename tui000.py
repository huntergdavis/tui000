import os
import shutil
import sys
import asyncio

from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static
from textual.events import Key

from package.headshot import Headshot
from package.lifemap import LifeMap
from package.progressbar import ProgressBar
from package.eventlog import EventLog
from package.questionbox import QuestionBox
from package.character import Character
from package.lifequestions import LifeEventQuestions


class Tui000(App):

    CSS_PATH = os.path.join(os.path.dirname(__file__), "package", "tui000.css")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize widgets
        self.question_box = QuestionBox(id="question_box")
        self.progress_bar = ProgressBar(id="progress_bar")
        self.event_log = EventLog(id="event_log")

        # Create an instance of Character to hold character data
        self.character = Character()

        # Create the LifeMap widget, pass the character's life_map_data
        self.life_map_widget = LifeMap(
            life_map_data=self.character.life_map_data,
            id="life_map_widget"
        )

        # Create the Headshot widget using the character instance
        self.headshot_widget = Headshot(
            character=self.character,
            id="headshot_widget"
        )

        # Create the menu
        menu_content = "([b]G[/b]raveyard) ([b]O[/b]ptions) ([b]R[/b]efresh) ([b]Q[/b]uit)"
        self.menu = Static(menu_content, id="menu")

    def compose(self) -> ComposeResult:
        # Middle container with headshot, question box, and life map
        with Horizontal(id="middle_container"):
            # Left container with headshot
            with Vertical(id="left_container"):
                yield self.headshot_widget
            # Center container with question box and other widgets
            with Vertical():
                yield self.question_box
                yield self.event_log
                yield self.progress_bar
                yield self.menu
            # Right container with life map
            with Vertical(id="right_container"):
                yield self.life_map_widget

    async def on_mount(self) -> None:
        # Initial setup
        await self.refreshQuestions()
        self.set_interval(10, self.refreshQuestions)  # Refresh questions every 10 seconds
        self.event_log.add_entry("App started.")
        self.event_log.add_entry(f"Welcome, {self.character.bio.name}!")
        self.event_log.add_entry("Waiting for user input...")
        # Start the progress bar
        await self.progress_bar.start()

    async def refreshQuestions(self):
        question_and_answers = LifeEventQuestions.get_random_question()
        self.question = question_and_answers['question']
        self.choices = question_and_answers['choices']
        await self.question_box.display_question(self.question, self.choices)

    async def action_debug(self) -> None:
        # Add debug information to the event log
        terminal_size = shutil.get_terminal_size((80, 24))
        width, height = terminal_size.columns, terminal_size.lines
        debug_content = f"Terminal size: {width}x{height}"
        self.event_log.add_entry(debug_content)
        self.event_log.scroll_down()

    async def refresh_character(self):
        # Refresh the character data
        self.character.refresh()

        # Update the Headshot widget with new headshot data
        self.headshot_widget.face_text = self.character.headshot_text

        # Update the LifeMap widget with new life map data
        self.life_map_widget.update_life_map(self.character.life_map_data)

        # Log the refresh
        self.event_log.add_entry("Character refreshed.")
        self.event_log.scroll_down()

        # Refresh the question box with a new question
        await self.refreshQuestions()

    async def on_key(self, event: Key) -> None:
        await self.question_box.on_key(event)  # Handle key events in the question box

        # Log the key press
        self.event_log.add_entry(f"Key '{event.key}' pressed.")
        self.event_log.scroll_down()

        # Handle special keys
        if event.key.lower() == "q":
            self.exit()  # Exit the application
        elif event.key.lower() == "o":
            await self.action_debug()
            await self.refreshQuestions()
        elif event.key.lower() == "r":
            await self.refresh_character()
        elif event.key == "up":
            for _ in range(5):
                self.event_log.scroll_up()
        elif event.key == "down":
            for _ in range(5):
                self.event_log.scroll_down()

    async def on_ready(self) -> None:
        print("App is ready. Press 'q' to quit.")


if __name__ == "__main__":
    try:
        app = Tui000()
        if len(sys.argv) > 1 and sys.argv[1] == "-log":
            app.run(log="textual.log")
        else:
            app.run()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
    except asyncio.CancelledError:
        print("The application was cancelled.", file=sys.stderr)
