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
        """Generate the headshot and bio and store it in self.headshot_text."""
        face_size = 18  # Size of the headshot

        # Initialize the grid with empty spaces
        headshot = [[" " for _ in range(face_size)] for _ in range(face_size)]

        # Randomly decide if we're using a background color or an outline
        use_background = random.choice([True, False])

        if not use_background:
            self.add_outline(headshot, face_size)  # Add outline if no background is used

        # Generate hairstyles and place them in the grid
        hairstyle_char, hairstyle_color = self.generate_hairstyles(headshot, face_size)

        # Generate eyebrows and place them in the grid
        eyebrows_char, eyebrows_color = self.generate_eyebrows(headshot, face_size)

        # Generate facial features and place them in the grid
        (eye_char, eye_color, nose_char, nose_color, mouth_chars, mouth_color,
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
            mouth_chars, mouth_color, face_fill_char, face_color,
            hairstyle_char, hairstyle_color, eyebrows_char, eyebrows_color,
            bg_color
        )

        # Cache the headshot without bio by making a deep copy
        self.headshot_text_cache = self.headshot_text.copy()

        # Append bio information below the face
        self.generate_bio(self.headshot_text)

    def add_outline(self, grid: list, face_size: int) -> None:
        """Add an outline around the face."""
        for i in range(face_size):
            grid[i][0] = "|"
            grid[i][face_size - 1] = "|"
        for j in range(face_size):
            grid[0][j] = "-"
            grid[face_size - 1][j] = "-"

    def generate_facial_features(self, grid: list, face_size: int) -> tuple:
        """
        Generate and place facial features on the grid.

        Returns:
            A tuple containing characters and their corresponding colors for eyes, nose, mouth,
            face fill, and face color.
        """
        colors = ["cyan", "light_blue", "green", "magenta", "yellow", "light_green"]

        # Characters to represent different parts of the face
        eyes = ["O", "@", "*", "o"]
        mouth_styles = {
            'smile': [
                "  \\___/  ",
                "         ",
                "         "
            ],
            'frown': [
                "  /___\\  ",
                "         ",
                "         "
            ],
            'neutral': [
                "  -----  ",
                "         ",
                "         "
            ],
            'grin': [
                " :D___D: ",
                "         ",
                "         "
            ],
            'angry': [
                " >___<  ",
                "         ",
                "         "
            ]
        }

        nose = ["|", "^", "v"]
        face_fill = [".", " "]

        # Generate random features
        eye_char = random.choice(eyes)
        eye_color = random.choice(colors)
        nose_char = random.choice(nose)
        nose_color = random.choice(colors)
        mouth_style = random.choice(list(mouth_styles.keys()))
        mouth_lines = mouth_styles[mouth_style]
        mouth_chars = set(char for line in mouth_lines for char in line if char.strip())
        mouth_color = random.choice(colors)
        face_fill_char = random.choice(face_fill)
        face_color = random.choice(colors)

        # Place eyes and nose in the grid
        grid[4][5] = eye_char
        grid[4][12] = eye_char
        grid[9][8] = nose_char
        grid[9][9] = nose_char

        # Place mouth in the grid (multi-line, shifted left)
        # mouth start col should be random between 3 and 6
        mouth_start_col = random.randint(3, 6)
        mouth_start_row = 13
        for row_offset, line in enumerate(mouth_lines):
            row = mouth_start_row + row_offset
            for col_offset, char in enumerate(line):
                grid[row][mouth_start_col + col_offset] = char

        return (eye_char, eye_color, nose_char, nose_color,
                list(mouth_chars), mouth_color, face_fill_char, face_color)

    def generate_eyebrows(self, grid: list, face_size: int) -> tuple:
        """
        Generate and place eyebrows on the grid.

        Returns:
            A tuple containing the eyebrows characters and their corresponding color.
        """
        eyebrow_styles = ["///", "^^^", "---", "~~~", "***"]
        eyebrow_char = random.choice(eyebrow_styles)
        eyebrow_color = random.choice(["brown", "black", "grey", "dark_blue", "dark_green"])

        # Place left eyebrow
        for idx, char in enumerate(eyebrow_char):
            grid[3][4 + idx] = char

        # Place right eyebrow
        for idx, char in enumerate(eyebrow_char):
            grid[3][11 + idx] = char

        return (eyebrow_char, eyebrow_color)  # Representative characters for styling

    def generate_hairstyles(self, grid: list, face_size: int) -> tuple:
        """
        Generate and place hairstyles on the grid.

        Returns:
            A tuple containing the hairstyle character and its corresponding color.
        """
        hairstyles = [
            {"style": "short", "chars": ["^", "^", "^"], "color": "yellow"},
            {"style": "long", "chars": ["~", "~", "~"], "color": "brown"},
            {"style": "curly", "chars": ["@", "@", "@"], "color": "orange"},
            {"style": "ponytail", "chars": ["V", "V", "V"], "color": "red"},
            {"style": "spiky", "chars": ["*", "*", "*"], "color": "light_magenta"}
        ]

        selected_hairstyle = random.choice(hairstyles)
        hairstyle_chars = selected_hairstyle["chars"]
        hairstyle_color = selected_hairstyle["color"]

        # Define the starting row for hairstyles
        hairstyle_start_row = 1

        for row_offset, char in enumerate(hairstyle_chars):
            row = hairstyle_start_row + row_offset
            for col in range(face_size):
                # Randomly decide whether to place a hair character or leave it empty
                if random.choice([True, False, False]):  # Adjust probability as needed
                    grid[row][col] = char

        # For styling purposes, use the first character as representative
        hairstyle_char = hairstyle_chars[0]

        return hairstyle_char, hairstyle_color

    def fill_face(self, grid: list, face_fill_char: str, face_size: int) -> None:
        """Fill the empty spaces in the face with the face_fill_char."""
        for i in range(face_size):
            for j in range(face_size):
                if grid[i][j] == " ":
                    grid[i][j] = face_fill_char

    def grid_to_rich_text(self, grid: list, face_size: int, eye_char: str, eye_color: str,
                          nose_char: str, nose_color: str, mouth_chars: list,
                          mouth_color: str, face_fill_char: str, face_color: str,
                          hairstyle_char: str, hairstyle_color: str,
                          eyebrows_char: str, eyebrows_color: str,
                          bg_color: str) -> Text:
        """
        Convert the grid to a Rich Text object with appropriate styling.

        Args:
            grid (list): The headshot grid.
            face_size (int): Size of the face grid.
            eye_char (str): Character representing the eyes.
            eye_color (str): Color for the eyes.
            nose_char (str): Character representing the nose.
            nose_color (str): Color for the nose.
            mouth_chars (list): Characters representing the mouth.
            mouth_color (str): Color for the mouth.
            face_fill_char (str): Character used to fill the face.
            face_color (str): Color for the face fill.
            hairstyle_char (str): Character representing the hairstyle.
            hairstyle_color (str): Color for the hairstyle.
            eyebrows_char (str): String representing the eyebrow characters.
            eyebrows_color (str): Color for the eyebrows.
            bg_color (str): Background color.

        Returns:
            Text: A Rich Text object representing the styled headshot.
        """
        face_text = Text()
        for i in range(face_size):
            for j in range(face_size):
                char = grid[i][j]
                if char == eye_char:
                    face_text.append(char, style=f"{eye_color} {bg_color}")
                elif char == nose_char:
                    face_text.append(char, style=f"{nose_color} {bg_color}")
                elif char in mouth_chars:
                    face_text.append(char, style=f"{mouth_color} {bg_color}")
                elif char in eyebrows_char:
                    face_text.append(char, style=f"{eyebrows_color} {bg_color}")
                elif char == hairstyle_char:
                    face_text.append(char, style=f"{hairstyle_color} {bg_color}")
                elif char in ["-", "|"]:  # Border chars
                    face_text.append(char, style="grey58")  # Outline in a neutral color
                else:
                    face_text.append(char, style=f"{face_color} {bg_color}")
            face_text.append("\n")
        return face_text

    def center_text(self, text: str, width: int = 18) -> str:
        """Center the given text within the specified width."""
        return text.center(width)

    def generate_bio(self, face_text: Text) -> None:
        """Append bio information below the face in the Rich Text object."""
        face_text.append(f"\n{self.center_text(self.bio.name)}\n", style="bold")
        face_text.append(f"{self.center_text(self.bio.profession)}\n", style="italic")
        face_text.append(f"{self.center_text(f'{self.bio.age} years old')}\n")
        face_text.append(f"{self.center_text(self.bio.life_focus)}\n", style="bold italic")

    def cached_headshot_and_bio(self) -> None:
        """Use the cached headshot text and regenerate the bio."""
        self.headshot_text = self.headshot_text_cache.copy()
        self.generate_bio(self.headshot_text)

    def incrementAge(self) -> None:
        """Increment the character's age and update the headshot and bio."""
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
            life_map_widget (LifeMap): The LifeMap instance containing life progression data.
        """
        # Ensure that the headshot_text has been generated
        if not hasattr(self, 'headshot_text'):
            raise ValueError("Headshot text has not been generated yet. Call generate_headshot_and_bio() first.")

        # Sort and reverse the life map's color_map
        color_map = life_map_widget.color_map
        color_map.sort()
        color_map.reverse()

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
                "color_map": color_map,       # List of colors corresponding to 'X's
                "current_index": life_map_widget.current_index  # Current progress index
            }
        }

        # Get the current timestamp in a filename-friendly format
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Make graveyard directory if it does not exist
        if not os.path.exists("./graveyard"):
            os.makedirs("./graveyard")

        # The filename is the name of the character and the timestamp in filename friendly format
        filename = f"./graveyard/{self.bio.name.replace(' ', '_')}_{timestamp}.json"

        try:
            # Write the data to the specified JSON file with indentation for readability
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Character state successfully saved to {filename}.")
        except Exception as e:
            print(f"Failed to save character state to {filename}: {e}")
