from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text
import random

class Headshot(Widget):
    character_name = reactive("")
    profession = reactive("")
    age = reactive(0)
    focus = reactive("")
    face_text = reactive(Text())
    face_size: int = 18  # Renamed from 'size' to 'face_size'

    def __init__(self, character_name, profession, age, focus, **kwargs):
        super().__init__(**kwargs)
        self.character_name = character_name
        self.profession = profession
        self.age = age
        self.focus = focus
        self.face_text = Text()
        self.generate_headshot_and_bio()

    def watch_character_name(self, old_value, new_value):
        self.generate_headshot_and_bio()

    def watch_profession(self, old_value, new_value):
        self.generate_headshot_and_bio()

    def watch_age(self, old_value, new_value):
        self.generate_headshot_and_bio()

    def watch_focus(self, old_value, new_value):
        self.generate_headshot_and_bio()

    def generate_headshot_and_bio(self) -> None:
        # Initialize the grid
        headshot = self.initialize_grid()

        # Randomly decide if we're using a background color or an outline
        use_background = random.choice([True, False])

        if not use_background:
            self.add_outline(headshot)  # Add outline if no background is used

        # Generate facial features and place them in the grid
        (eye_char, eye_color, nose_char, nose_color, mouth_char, mouth_color,
         face_fill_char, face_color) = self.generate_facial_features(headshot)

        # Optionally use a background color
        bg_color = random.choice(
            ["on_black", "on_white", "on_grey19", "on_cornsilk1", "on_dark_blue"]
        ) if use_background else ""

        # Fill the face with the background pattern
        self.fill_face(headshot, face_fill_char)

        # Convert the grid to rich text with coloring
        self.face_text = self.grid_to_rich_text(
            headshot, eye_char, eye_color, nose_char, nose_color,
            mouth_char, mouth_color, face_fill_char, face_color, bg_color
        )

        # Append bio information below the face
        self.generate_bio(self.face_text)

    def render(self) -> Text:
        """Render the headshot and bio."""
        return self.face_text

    def initialize_grid(self) -> list:
        return [[" " for _ in range(self.face_size)] for _ in range(self.face_size)]

    def add_outline(self, grid: list) -> None:
        for i in range(self.face_size):
            grid[i][0] = "|"
            grid[i][self.face_size - 1] = "|"
        for j in range(self.face_size):
            grid[0][j] = "-"
            grid[self.face_size - 1][j] = "-"

    def generate_facial_features(self, grid: list) -> tuple:
        colors = ["cyan", "light_blue", "green", "magenta", "yellow", "light_green"]

        # Characters to represent different parts of the face
        eyes = ["O", "@", "*", "o"]
        mouth = ["-", "=", "~"]
        nose = ["|", "^", "v"]
        face_fill = [".", " "]

        # Generate random features
        eye_char = random.choice(eyes)
        eye_color = random.choice(colors)
        nose_char = random.choice(nose)
        nose_color = random.choice(colors)
        mouth_char = random.choice(mouth)
        mouth_color = random.choice(colors)
        face_fill_char = random.choice(face_fill)
        face_color = random.choice(colors)

        # Place eyes, nose, and mouth in the grid
        grid[4][5] = eye_char
        grid[4][12] = eye_char
        grid[9][8] = nose_char
        grid[9][9] = nose_char
        for i in range(6, 12):
            grid[14][i] = mouth_char

        return (eye_char, eye_color, nose_char, nose_color,
                mouth_char, mouth_color, face_fill_char, face_color)

    def fill_face(self, grid: list, face_fill_char: str) -> None:
        for i in range(self.face_size):
            for j in range(self.face_size):
                if grid[i][j] == " ":
                    grid[i][j] = face_fill_char

    def grid_to_rich_text(self, grid: list, eye_char: str, eye_color: str,
                          nose_char: str, nose_color: str, mouth_char: str,
                          mouth_color: str, face_fill_char: str, face_color: str,
                          bg_color: str) -> Text:
        face_text = Text()
        for i in range(self.face_size):
            for j in range(self.face_size):
                char = grid[i][j]
                if char == eye_char:
                    face_text.append(char, style=f"{eye_color} {bg_color}")
                elif char == nose_char:
                    face_text.append(char, style=f"{nose_color} {bg_color}")
                elif char == mouth_char:
                    face_text.append(char, style=f"{mouth_color} {bg_color}")
                elif char in ["-", "|"]:  # Border chars
                    face_text.append(char, style="grey58")  # Outline in a neutral color
                else:
                    face_text.append(char, style=f"{face_color} {bg_color}")
            face_text.append("\n")
        return face_text

    def center_text(self, text: str, width: int = 18) -> str:
        return text.center(width)

    def generate_bio(self, face_text: Text) -> None:
        face_text.append(f"\n{self.center_text(self.character_name)}\n", style="bold")
        face_text.append(f"{self.center_text(self.profession)}\n", style="italic")
        face_text.append(f"{self.center_text(f'{self.age} years old')}\n")
        face_text.append(f"{self.center_text(self.focus)}\n", style="bold italic")
