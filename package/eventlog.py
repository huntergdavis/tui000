from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text

class EventLog(Widget):
    log_entries = reactive("")
    scroll_position = reactive(0)  # Track the current scroll position
    style = "gray"  # Default style for the log entries

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.log_entries_list = []  # Store the log entries as a list of strings
        self.visible_lines = 4  # Number of lines visible in the log (5 by default)

    def on_mount(self) -> None:
        """Called when the widget is added to the app."""
        self.update_log()

    def add_entry(self, entry: str) -> None:
        """Add an entry to the log and refresh the display."""
        self.log_entries_list.append(entry)  # Add the new entry
        self.update_log()

    def update_log(self) -> None:
        """Update the widget with the currently visible log entries."""
        # Adjust the visible portion of the log based on the scroll position
        start = max(0, self.scroll_position)
        end = min(len(self.log_entries_list), self.scroll_position + self.visible_lines)
        visible_entries = self.log_entries_list[start:end]

        # Join all visible log entries into one string with newlines
        log_content = "\n".join(visible_entries)
        self.log_entries = log_content  # Update the reactive value
        self.refresh()  # Refresh the widget to reflect the new content

    def scroll_down(self) -> None:
        """Scroll down in the log, if possible."""
        if self.scroll_position < len(self.log_entries_list) - self.visible_lines:
            self.scroll_position += 1
        self.update_log()

    def scroll_up(self) -> None:
        """Scroll up in the log, if possible."""
        if self.scroll_position > 0:
            self.scroll_position -= 1
        self.update_log()

    def set_log_color(self, color: str) -> None:
        """Change the color of the log entries."""
        self.style = color

    def render(self) -> Text:
        """Render the log content as rich text with a position indicator."""
        total_entries = len(self.log_entries_list)

        # Prepare the content for the log
        log_text = Text(self.log_entries, style=self.style)

        # Create position indicator
        start_position = self.scroll_position + 1
        end_position = min(self.scroll_position + self.visible_lines, total_entries)

        # Build the complete log output
        output = Text()

        # Add the log entries
        output.append(log_text)

        # Add the position indicator below the log entries
        output.append(f"\n{start_position} - {end_position} / {total_entries} ", style="bold green")

        return output
