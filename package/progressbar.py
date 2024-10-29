########################################################################################
# 2024-10-29
# Somehow accidentally UNDID the changes I made yesterday causing it to break
# Managed to restore the proper version that works.
# Jds
#
########################################################################################

from textual.widget import Widget
from textual.reactive import Reactive
from rich.text import Text
import asyncio
import random


class ProgressBar(Widget):
    percentage: Reactive[int] = Reactive(100)  # Start at 100%
    color: Reactive[str] = Reactive("cyan")  # Start with cyan


    # Define colors as reactive property
    colors = Reactive([
        "dark_cyan",
        "dim_gray",
        "dark_slate_gray1",
        "cadet_blue",
        "slate_gray"
    ])
    
    def __init__(self):
        super().__init__()
        self._running = False  # Control variable for animation


        # Define a list of muted related colors
        self.colors = [
            "dark_cyan", "dim_gray", "dark_slate_gray1", "cadet_blue", "slate_gray"
        ]


    def generate_bar(self) -> Text:
        """
        Generate a colored bar of 39 characters long and 3 characters high.
        Fill based on the current percentage (0-100).
        """
        bar_length = 39
        fill_length = int((self.percentage / 100) * bar_length)


        filled_part = "█" * fill_length  # Use '█' for the filled portion
        empty_part = " " * (bar_length - fill_length)  # Empty portion of the bar


        # Bar will be 3 lines high, using the current color
        bar = Text()
        for _ in range(3):
            bar.append(f"{filled_part}{empty_part}\n", style=self.color)
        
        return bar


    async def on_mount(self) -> None:
        """Called when the widget is added to the app."""
        self.refresh()


    def render(self) -> Text:
        """Render the progress bar when the widget is displayed."""
        return self.generate_bar()


    async def start(self) -> None:
        """Start the automatic countdown."""
        if not self._running:
            self._running = True
            self.set_interval(5, self.decrease_progress)  # Schedule decrease every 5 second


    async def stop(self) -> None:
        """Stop the automatic countdown."""
        self._running = False


    async def decrease_progress(self) -> None:
        """Decrease the progress bar by 10% every second."""
        if self._running and self.percentage > 0:
            self.percentage = max(0, self.percentage - 10)
            self.refresh()


        if self.percentage == 0:
            # Choose a new random color when the bar reaches 0
            self.color = random.choice(self.colors)
            self.percentage = 100  # Reset the progress bar to 100%
            self.refresh()


    async def reset(self) -> None:
        """Reset the progress bar to 100% and stop the countdown."""
        self.percentage = 100
        self._running = False
        self.refresh()
