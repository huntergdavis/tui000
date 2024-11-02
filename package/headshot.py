# headshot.py
from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text

class Headshot(Widget):
    face_text = reactive(Text())

    def __init__(self, character, **kwargs):
        super().__init__(**kwargs)
        self.character = character
        self.face_text = self.character.headshot_text

    def render(self) -> Text:
        """Render the headshot and bio."""
        return self.face_text
