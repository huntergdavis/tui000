# progressbar.py
from textual.widgets import Static  # Corrected import path
from textual.reactive import reactive
from rich.text import Text
import random

class ProgressBar(Static):
    """
    ProgressBar widget displays a progress bar that ticks down over time.
    """
    
    # Define reactive properties for percentage and color
    percentage = reactive(100)  # Start at 100%
    color = reactive("cyan")    # Start with cyan

    def __init__(self, **kwargs):
        """
        Initialize the ProgressBar.
        
        Args:
            **kwargs: Additional keyword arguments for the Widget.
        """
        super().__init__(**kwargs)
        
        # Define color options for cycling
        self.color_options = [
            "dark_cyan", "dim_gray", "dark_slate_gray1", "cadet_blue", "slate_gray"
        ]

    def generate_bar(self) -> Text:
        """
        Generate a colored bar of 39 characters long and 3 characters high.
        Fill based on the current percentage (0-100).
        
        Returns:
            Text: The rich Text object representing the progress bar.
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

    def on_mount(self) -> None:
        """
        Called when the widget is added to the app.
        Starts the automatic countdown.
        """
        print("ProgressBar mounted.")
        self.refresh()
        
    def render(self) -> Text:
        """
        Render the progress bar when the widget is displayed.
        
        Returns:
            Text: The rich Text object representing the progress bar.
        """
        return self.generate_bar()



    def decrease_progress(self) -> None:
        """
        Decrease the progress bar by 10% every interval.
        When the percentage reaches 0%, choose a new random color and reset to 100%.
        """
        print("ProgressBar decrease_progress called.")
        if self.percentage > 0:
            self.percentage = max(0, self.percentage - 10)
            print(f"ProgressBar percentage decreased to {self.percentage}%")
            self.refresh()

        if self.percentage == 0:
            # Choose a new random color when the bar reaches 0
            self.color = random.choice(self.color_options)
            print(f"ProgressBar color changed to {self.color}")
            self.percentage = 100  # Reset the progress bar to 100%
            print("ProgressBar percentage reset to 100%")
            self.refresh()

    def reset_progress(self) -> None:
        """
        Reset the progress bar to 100% and stop the countdown.
        """
        self.percentage = 100
        self.color = "cyan"  # Reset to the initial color
        print("ProgressBar reset to 100% and stopped.")
        self.refresh()
