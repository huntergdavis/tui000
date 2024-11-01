from textual.widget import Widget
from textual.reactive import reactive
from textual.events import Key

from rich.text import Text


class QuestionBox(Widget):
    question = reactive("")
    choices = reactive([])
    selected_choice = reactive("")  # Store the selected choice
    max_line_length: int = 36  # Maximum line length for the box

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    async def display_question(self, question: str, choices: list) -> None:
        """Display a multiple-choice question with choices."""
        self.question = question
        self.choices = choices
        self.selected_choice = ""
        self.refresh()  # Refresh to show the question and choices

    async def clear(self) -> None:
        """Clear the question box."""
        self.question = ""
        self.choices = []
        self.selected_choice = ""
        self.refresh()  # Refresh to clear the box

    async def on_key(self, event: Key) -> None:
        """Handle key events for user input."""
        if event.key in [choice[0].lower() for choice in self.choices]:
            self.selected_choice = event.key
            await self.clear()  # Clear the box after selection

    def render(self) -> Text:
        """Render the question box."""
        box_lines = ["+-" + "-" * self.max_line_length + "+"]  # Top border

        if self.question:
            # Split the question into multiple lines based on max_line_length
            question_lines = self.split_text_into_lines(self.question, self.max_line_length)
            for line in question_lines:
                box_lines.append(f"| {line.ljust(self.max_line_length)} |")  # Add each line with padding
        else:
            box_lines.append(f"|{' ' * self.max_line_length}|")  # Empty line for spacing

        # Add choices directly below the question
        for choice in self.choices:
            choice_text = f"{choice[0].upper()}: {choice[1]}"
            box_lines.append(f"| {choice_text.ljust(self.max_line_length)} |")

        box_lines.append("+-" + "-" * self.max_line_length + "+")  # Bottom border

        return Text("\n".join(box_lines), style="blue")

    def split_text_into_lines(self, text: str, max_length: int) -> list:
        """Split a text into lines with a maximum length."""
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= max_length:  # +1 for space
                if current_line:
                    current_line += " "
                current_line += word
            else:
                lines.append(current_line)
                current_line = word

        if current_line:  # Add any remaining text as a line
            lines.append(current_line)

        # Ensure each line is right-padded to match max_line_length
        return [line.ljust(max_length) for line in lines]
