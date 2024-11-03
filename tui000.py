import os
import shutil
import sys
import asyncio
import logging

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
from package.lifeevents import LifeEvents


class Tui000(App):
    """
    Main application class.
    """

    CSS_PATH = os.path.join(os.path.dirname(__file__), "package", "tui000.css")

    def __init__(self, debug_mode=False, **kwargs):
        super().__init__(**kwargs)

        # Set tic_rate based on debug_mode flag
        self.debug_mode = debug_mode
        if self.debug_mode:
            self.tic_rate = 0.002  # Faster refresh rate for debugging
        else:
            self.tic_rate = 2  # Normal refresh rate

        # set current tic to 0
        self.current_tic = 1

        # Initialize widgets
        self.question_box = QuestionBox(id="question_box")
        self.progress_bar = ProgressBar(id="progress_bar")
        self.event_log = EventLog(id="event_log")

        # Create an instance of Character to hold character data
        self.character = Character()

        # Create the LifeMap widget
        self.life_map_widget = LifeMap(id="life_map_widget")

        # Create the Headshot widget using the character instance
        self.headshot_widget = Headshot(
            character=self.character,
            id="headshot_widget"
        )

        # Create the LifeEvents instance
        self.life_events = LifeEvents()

        # Initialize lifequestions instance
        self.life_questions = LifeEventQuestions()

        # Create the menu
        menu_content = "([b]G[/b]raveyard) ([b]O[/b]ptions) ([b]R[/b]espawn) ([b]Q[/b]uit)"
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
        """
        Called when the application mounts.
        """
        # Initial setup
        await self.refreshQuestions()
        self.set_interval(self.tic_rate, self.moveGameLoopForwardOrDie)  # Refresh questions every tic_rate seconds
        self.log_message("App started.")
        self.log_message(f"Welcome, {self.character.bio.name}!")
        self.log_message("Waiting for user input...")
        # Do NOT call self.progress_bar.start() here

    async def refreshQuestions(self):
        """
        Fetch and display a new question.
        """
        question_and_answers = self.life_questions.get_random_question()
        self.question = question_and_answers['question']
        self.choices = question_and_answers['choices']
        await self.question_box.display_question(self.question, self.choices)
        # Log the question if debug mode is enabled
        if self.debug_mode:
            self.log_message(f"New question: {self.question}")

        # log the answers and their colors if debug is enabled
        if self.debug_mode:
            for choice in self.choices:
                self.log_message(f"{choice['text']} - {choice['color']}")

    async def moveGameLoopForwardOrDie(self):

        # increment current tic, the heartbeat of the game
        self.current_tic += 1

        # 3/4 of the time, display as normal, but the last 1/4 display the highlighted entry
        if self.current_tic % 8 == 0:
            self.question_box.highlightselectedanswer()
            self.log_message(f"{self.character.bio.name} chose {self.question_box.getselectedcategory()}")
        
        if self.current_tic % 10 == 0:
            # Check for life event
            life_event = self.life_events.checkforlifeevent(self.character)
            if life_event == "death":
                self.log_message("A fatal life event occurred.")
                await self.handle_death_event()
            else:
                self.life_map_widget.increment_progress(self.question_box.getselectedcolor())
                self.progress_bar.decrease_progress()
                self.headshot_widget.incrementAge()
                self.log_message(f"Age incremented to {self.character.bio.age}")
                """
                Refresh questions, handle life events, and update progress in LifeMap.
                """
                await self.refreshQuestions()

    async def handle_death_event(self):
        """
        Handle the character's death event.
        """
        self.log_message("Oh no! Your character has passed away.")
        await self.refresh_character()

    async def action_debug(self) -> None:
        """
        Add debug information to the event log.
        """
        # Add debug information to the event log
        terminal_size = shutil.get_terminal_size((80, 24))
        width, height = terminal_size.columns, terminal_size.lines
        debug_content = f"Terminal size: {width}x{height}"
        self.log_message(debug_content)

    async def refresh_character(self):
        """
        Refresh the character's data and update widgets accordingly.
        """
        # Refresh the character data
        self.character.refresh()

        # Update the Headshot widget with new headshot data
        self.headshot_widget.face_text = self.character.headshot_text

        # Update the LifeMap widget with new life map data
        self.life_map_widget.reset_progress()

        # Log the refresh
        self.log_message("Character re-spawned.")

        # Refresh the question box with a new question
        await self.refreshQuestions()

        # Refresh the life map
        self.life_map_widget.refresh()

        # Reset the progress bar
        self.progress_bar.reset_progress()

    # handle in-app and out of app logging
    def log_message(self, message: str, level: str = "info") -> None:
        """
        Log a message to the event log and to the tui000.log file.

        Args:
            message (str): The message to log.
            level (str): The severity level of the log ('debug', 'info', 'warning', 'error', 'critical').
        """
        # Log to the event log within the TUI
        self.event_log.add_entry(message)
        self.event_log.scroll_down()

        # if debug
        if self.debug_mode:
            # Log to the file using the logging module
            if level.lower() == "debug":
                logging.debug(message)
            elif level.lower() == "info":
                logging.info(message)
            elif level.lower() == "warning":
                logging.warning(message)
            elif level.lower() == "error":
                logging.error(message)
            elif level.lower() == "critical":
                logging.critical(message)
            else:
                logging.info(message)  # Default to INFO if unknown level

    async def on_key(self, event: Key) -> None:
        """
        Handle key press events.
        """
        await self.question_box.on_key(event)  # Handle key events in the question box

        # Log the key press
        self.log_message(f"Key '{event.key}' pressed.")
        self.event_log.scroll_down()

        # Handle special keys
        if event.key.lower() == "q":
            self.exit()  # Exit the application
        elif event.key.lower() == "o":
            await self.action_debug()
            await self.refreshQuestions()
        elif event.key.lower() == "r":
            self.current_tic = 1;
            await self.refresh_character()
        elif event.key == "up":
            for _ in range(5):
                self.event_log.scroll_up()
        elif event.key == "down":
            for _ in range(5):
                self.event_log.scroll_down()

    async def on_ready(self) -> None:
        """
        Called when the application is ready.
        """
        print("App is ready. Press 'q' to quit.")


if __name__ == "__main__":
    try:
        # Determine if debug flag is set via command line
        debug_mode = False
        if len(sys.argv) > 1 and sys.argv[1] == "-debug":
            debug_mode = True
            # Configure logging based on debug_mode
            logging.basicConfig(
                level=logging.DEBUG if debug_mode else logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler("tui000.log"),
                    #logging.StreamHandler(sys.stdout)  # Optional: Keep this if you still want some output in terminal
                ]
            )

        # Initialize the application with the debug flag
        app = Tui000(debug_mode=debug_mode)

        # Run the application
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
    except asyncio.CancelledError:
        print("The application was cancelled.", file=sys.stderr)
