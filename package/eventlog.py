from textual.widget import Widget
from textual.reactive import Reactive
from rich.text import Text

class EventLog(Widget):
    log_entries: Reactive[str] = Reactive("")

    def __init__(self) -> None:
        super().__init__()
        self.log_entries_list = []  # Store the log entries as a list of strings

    async def on_mount(self) -> None:
        """Called when the widget is added to the app."""
        await self.update_log()

    async def add_entry(self, entry: str) -> None:
        """Add an entry to the log and refresh the display."""
        self.log_entries_list.append(entry)  # Add the new entry
        if len(self.log_entries_list) > 5:  # Limit the log to the last 5 entries
            self.log_entries_list.pop(0)  # Remove the oldest entry
        await self.update_log()

    async def update_log(self) -> None:
        """Update the widget with the current log entries."""
        # Join all log entries into one string with newlines
        log_content = "\n".join(self.log_entries_list)
        # Store the content as Reactive, which automatically triggers a refresh
        self.log_entries = log_content
        self.refresh()  # Refresh the widget to reflect the new content

    def render(self) -> Text:
        """Render the log content as rich text."""
        return Text(self.log_entries, style="green")
