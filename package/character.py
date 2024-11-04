# character.py
from datetime import datetime
import os
from package.bio import Bio
from rich.text import Text
import random
import json

class Character:
    def __init__(self):
        # Store the generated headshot so it can be used later when the age is updated
        self.headshot_text_cache = Text()
        self.refresh()  # Initialize by refreshing character data

    def generate_headshot_and_bio(self) -> None:
        # Generate the headshot and bio and store it in self.headshot_text
        face_size = 18  # Size of the headshot

        # Initialize the grid
        headshot = [[" " for _ in range(face_size)] for _ in range(face_size)]

        # Randomly decide if we're using a background color or an outline
        use_background = random.choice([True, False])

        if not use_background:
            self.add_outline(headshot, face_size)  # Add outline if no background is used

        # Generate facial features and place them in the grid
        (eye_char, eye_color, nose_char, nose_color, mouth_char, mouth_color,
         face_fill_char, face_color) = self.generate_facial_features(headshot, face_size)

        # Optionally use a background color
        bg_color = random.choice(
            ["on_black", "on_white", "on_grey19", "on_cornsilk1", "on_dark_blue"]
        ) if use_background else ""

        # Fill the face with the background pattern
        self.fill_face(headshot, face_fill_char, face_size)

        # Convert the grid to rich text with coloring
        self.headshot_text = self.grid_to_rich_text(
            headshot, face_size, eye_char, eye_color, nose_char, nose_color,
            mouth_char, mouth_color, face_fill_char, face_color, bg_color
        )

        # Cache the headshot without bio by making a deep copy
        self.headshot_text_cache = self.headshot_text.copy()

        # Append bio information below the face
        self.generate_bio(self.headshot_text)

    def add_outline(self, grid: list, face_size: int) -> None:
        for i in range(face_size):
            grid[i][0] = "|"
            grid[i][face_size - 1] = "|"
        for j in range(face_size):
            grid[0][j] = "-"
            grid[face_size - 1][j] = "-"

    def generate_facial_features(self, grid: list, face_size: int) -> tuple:
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

    def fill_face(self, grid: list, face_fill_char: str, face_size: int) -> None:
        for i in range(face_size):
            for j in range(face_size):
                if grid[i][j] == " ":
                    grid[i][j] = face_fill_char

    def grid_to_rich_text(self, grid: list, face_size: int, eye_char: str, eye_color: str,
                          nose_char: str, nose_color: str, mouth_char: str,
                          mouth_color: str, face_fill_char: str, face_color: str,
                          bg_color: str) -> Text:
        face_text = Text()
        for i in range(face_size):
            for j in range(face_size):
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
        face_text.append(f"\n{self.center_text(self.bio.name)}\n", style="bold")
        face_text.append(f"{self.center_text(self.bio.profession)}\n", style="italic")
        face_text.append(f"{self.center_text(f'{self.bio.age} years old')}\n")
        face_text.append(f"{self.center_text(self.bio.life_focus)}\n", style="bold italic")

    def cached_headshot_and_bio(self) -> None:
        # Use a deep copy to prevent mutations from affecting the cache
        self.headshot_text = self.headshot_text_cache.copy()
        self.generate_bio(self.headshot_text)

    def incrementAge(self) -> None:
        self.bio.set_age(self.bio.age + 0.25)
        self.cached_headshot_and_bio()

    def refresh(self):
        """Refresh the character's data."""
        self.bio = Bio()  # Re-generate bio data
        self.generate_headshot_and_bio()  # Generate headshot and bio

    def save_to_json(self, life_map_widget) -> None:
        """
        Save the current state of the character, including bio and life map, to a JSON file.

        Args:
            filename (str): The path to the JSON file where data will be saved.
            life_map_widget (LifeMap): The LifeMap instance containing life progression data.
        """
        # Ensure that the headshot_text has been generated
        if not hasattr(self, 'headshot_text'):
            raise ValueError("Headshot text has not been generated yet. Call generate_headshot_and_bio() first.")

        # Prepare the data dictionary
        data = {
            "bio": {
                "name": self.bio.name,
                "profession": self.bio.profession,
                "age": self.bio.age,
                "life_focus": self.bio.life_focus
            },
            "headshot": self.headshot_text.plain,  # Convert Rich Text to plain string
            "life_map": {
                "color_map": life_map_widget.color_map,       # List of colors corresponding to 'X's
                "current_index": life_map_widget.current_index  # Current progress index
            }
        }

        # Get the current timestamp in a filename-friendly format
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # make graveyard directory if it does not exist
        if not os.path.exists("./graveyard"):
            os.makedirs("./graveyard")

        # the filename is the name of the character and the timestamp in filename friendly forma
        filename = f"./graveyard/{self.bio.name.replace(' ', '_')}_{timestamp}.json"

        try:
            # Write the data to the specified JSON file with indentation for readability
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Character state successfully saved to {filename}.")
        except Exception as e:
            print(f"Failed to save character state to {filename}: {e}")
