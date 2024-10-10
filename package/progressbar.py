from textual.app import App
from textual.widget import Widget
from textual.widgets import Static
from rich.text import Text

class ProgressBar(Widget):
    def __init__(self, percentage: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.percentage = percentage

    def generate_bar(self, percentage: int) -> Text:
        """
        Generate a cyan bar of 50 characters long and 3 characters high.
        Fill based on the provided percentage (0-100).
        """
        bar_length = 39
        fill_length = int((percentage / 100) * bar_length)
        
        filled_part = "█" * fill_length  # Use '█' for filled portion
        empty_part = " " * (bar_length - fill_length)  # Empty portion of the bar

        # Bar will be 3 lines high, so repeat the pattern 3 times
        bar = ""
        for _ in range(3):
            bar += f"[cyan]{filled_part}[/cyan]{empty_part}\n"  # Use cyan color

        # Return a Rich Text object that Textual understands
        return Text.from_markup(bar)

    async def on_mount(self) -> None:
        # Set the initial content for the progress bar
        self.refresh()

    def set_percentage(self, new_percentage: int):
        """Update the progress bar with a new percentage."""
        self.percentage = new_percentage
        self.refresh()

    def render(self) -> Text:
        """Render the progress bar when the widget is displayed."""
        return self.generate_bar(self.percentage)