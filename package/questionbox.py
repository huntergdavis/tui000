# questionbox.py

from textual.widget import Widget
from textual.reactive import reactive
from textual.events import Key

from rich.text import Text
from rich.style import Style

from random import randint


class QuestionBox(Widget):
    """
    A widget to display multiple-choice questions with color-coded choices
    and the ability to highlight a selected answer.
    """

    # Reactive variables to track the current question, choices, selected index, and selected color
    question = reactive("")
    choices = reactive([])  # List of dicts with 'label', 'text', 'color', 'life_category'
    selected_choice = reactive("")  # Store the selected choice (if needed)
    selected_index = reactive(None)  # Index of the choice to be highlighted (0-3)
    selected_color = reactive("")  # Color of the selected choice

    max_line_length: int = 36  # Maximum line length for the box

    def __init__(self, **kwargs) -> None:
        """
        Initialize the QuestionBox widget.

        Args:
            **kwargs: Additional keyword arguments for the Widget.
        """
        super().__init__(**kwargs)

        # set selected index to none
        self.selected_index = None

    async def display_question(self, question: str, choices: list) -> None:
        """
        Display a multiple-choice question with color-coded choices.

        Args:
            question (str): The question text.
            choices (list): A list of dictionaries, each containing:
                - 'label': Choice label (e.g., 'a')
                - 'text': Choice text (e.g., 'Red')
                - 'color': Color name (e.g., 'red')
                - 'life_category': Life category (e.g., 'Relationships')
        """
        self.question = question
        self.choices = choices
        self.selected_choice = ""  # Reset selected choice
        
        # set selected index to none
        self.selected_index = None

        self.refresh()  # Refresh the widget to display the new question

    async def clear(self) -> None:
        """
        Clear the question box by resetting question, choices, selected index, and selected color.
        """
        self.question = ""
        self.choices = []
        self.selected_choice = ""
        self.selected_index = None
        self.selected_color = ""
        self.refresh()  # Refresh the widget to clear the display

    async def on_key(self, event: Key) -> None:
        """
        Handle key events for user input.

        Args:
            event (Key): The key event.
        """
        # Example: Handle user input if needed
        # Uncomment and customize the following lines if you want to handle user selections
        """
        valid_keys = [choice['label'].lower() for choice in self.choices]
        if event.key.lower() in valid_keys:
            self.selected_choice = event.key.lower()
            # Emit an event or handle the selection as needed
            self.emit_no_wait("choice_selected", choice=self.selected_choice)
            await self.clear()  # Clear the box after selection
        """
        pass  # Currently, no user interaction is handled

    def highlightselectedanswer(self) -> None:
        """
        Highlight the selected answer based on a generated index.

        Raises:
            ValueError: If the index is not in [0, 1, 2, 3].
            IndexError: If the index is out of range for the available choices.
        """
        # set selected index to a random 0 to 3 value
        self.selected_index = randint(0, 3)

        if not isinstance(self.selected_index, int):
            raise TypeError("Index must be an integer.")
        if self.selected_index not in [0, 1, 2, 3]:
            raise ValueError("Index must be 0, 1, 2, or 3.")
        if self.selected_index >= len(self.choices):
            raise IndexError("Choice index out of range.")
        self.selected_index = self.selected_index
        # Update the selected_color based on the choice's color
        self.selected_color = self.choices[self.selected_index]['color']
        self.refresh()  # Refresh the widget to apply the highlight

    def getselectedcolor(self) -> str:
        """
        Get the color associated with the currently selected choice.

        Returns:
            str: The color name of the selected choice.

        Raises:
            ValueError: If no choice is currently selected.
        """
        if self.selected_index is None:
            raise ValueError("No choice is currently selected.")
        return self.selected_color

    def render(self) -> Text:
        """
        Render the question box with the question and color-coded choices,
        highlighting the selected choice if applicable.

        Returns:
            Text: The rendered text with styling.
        """
        box_text = Text()

        # Define styles
        border_style = Style(color="white")
        question_style = Style(color="white")
        highlight_bgcolor = "bright_white"  # Background color for highlighting

        # Top border
        top_border = f"+-{ '-' * self.max_line_length }-+"
        box_text += Text(top_border + "\n", style=border_style)

        # Question lines
        if self.question:
            question_lines = self.split_text_into_lines(self.question, self.max_line_length)
            for line in question_lines:
                line_content = f"| {line.ljust(self.max_line_length)} |"
                box_text += Text(line_content + "\n", style=question_style)
        else:
            box_text += Text(f"|{' ' * self.max_line_length}|", style=question_style) + Text("\n")

        # Choices
        for idx, choice in enumerate(self.choices):
            label = choice['label'].upper()
            text = choice['text']
            color = choice['color']

            # Ensure the color is a valid Rich color; default to white if not
            try:
                # Attempt to create a valid Rich Style
                choice_style = Style(color=color)
            except Exception:
                choice_style = Style(color="white")

            # Create the choice text
            choice_text = f"{label}: {text}"

            # Calculate padding
            padding_length = self.max_line_length - len(choice_text)
            if padding_length < 0:
                # Truncate if the choice_text exceeds max_line_length
                choice_text = choice_text[:self.max_line_length]
                padding_length = 0
            padding = ' ' * padding_length

            # Determine if this choice should be highlighted
            if self.selected_index == idx:
                # Apply highlight style (e.g., background color)
                line = Text("| ", style=border_style)
                line += Text(choice_text, style=Style(color=color, bgcolor=highlight_bgcolor))
                line += Text(padding + " |", style=border_style)
            else:
                # Regular choice styling
                line = Text("| ", style=border_style)
                line += Text(choice_text, style=choice_style)
                line += Text(padding + " |", style=border_style)

            box_text += line + Text("\n")

        # Bottom border
        bottom_border = f"+-{ '-' * self.max_line_length }-+"
        box_text += Text(bottom_border, style=border_style)

        return box_text

    def split_text_into_lines(self, text: str, max_length: int) -> list:
        """
        Split a text into lines with a maximum length.

        Args:
            text (str): The text to split.
            max_length (int): The maximum length of each line.

        Returns:
            list: A list of text lines.
        """
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
