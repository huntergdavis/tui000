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
        face_size = 18  # Size of the headshot grid

        # Initialize the grid with empty spaces
        self.grid = [[" " for _ in range(face_size)] for _ in range(face_size)]

        # Generate facial components
        self.generate_face_shape()
        self.generate_hairstyle()
        self.generate_eyes()
        self.generate_eyebrows()
        self.generate_nose()
        self.generate_mouth()
        self.generate_ears()
        self.generate_facial_hair()  # Optional facial hair
        self.generate_accessories()  # Glasses, earrings, piercings

        # Convert the grid to rich text with coloring
        self.headshot_text = self.grid_to_rich_text()

        # Cache the headshot without bio by making a deep copy
        self.headshot_text_cache = self.headshot_text.copy()

        # Append bio information below the face
        self.generate_bio(self.headshot_text)

    def generate_face_shape(self):
        """Define the face shape in the grid."""
        face_char = "░"  # Light shade block for skin
        face_color = random.choice(["light_yellow", "light_salmon1", "wheat1", "navajo_white1", "bisque1"])
        self.face_color = face_color

        # Define face boundaries (ellipse shape)
        for row in range(4, 14):
            for col in range(5, 13):
                if (row - 9) ** 2 + (col - 9) ** 2 <= 16:  # Circle equation
                    self.grid[row][col] = face_char

    def generate_hairstyle(self):
        """Generate and place the hairstyle on the grid."""
        hairstyles = [
            {"style": "short", "pattern": [" ██████ ", "████████"], "offset": -2},
            {"style": "medium", "pattern": ["  ████  ", " ██████ ", "████████"], "offset": -3},
            {"style": "long", "pattern": ["   ██   ", "  ████  ", " ██████ ", "████████"], "offset": -4},
            {"style": "curly", "pattern": ["  @@@@  ", " @@@@@@ ", "@@@@@@@@"], "offset": -3},
            {"style": "afro", "pattern": ["  ▓▓▓▓  ", " ▓▓▓▓▓▓ ", "▓▓▓▓▓▓▓▓"], "offset": -3},
            {"style": "bald", "pattern": [], "offset": 0}
        ]
        selected_hairstyle = random.choice(hairstyles)
        hair_pattern = selected_hairstyle["pattern"]
        hair_offset = selected_hairstyle["offset"]
        hair_colors = ["brown", "dark_red", "yellow", "grey69", "black", "light_blue", "purple", "green"]
        hair_color = random.choice(hair_colors)
        self.hair_color = hair_color

        start_row = 4 + hair_offset
        for i, line in enumerate(hair_pattern):
            row = start_row + i
            for j, char in enumerate(line):
                col = 5 + j
                if char != " ":
                    self.grid[row][col] = char

    def generate_eyes(self):
        """Generate and place the eyes on the grid."""
        eye_styles = [
            {"chars": ["●", "●"], "offset": 0},
            {"chars": ["◕", "◕"], "offset": 0},
            {"chars": ["⊙", "⊙"], "offset": 0},
            {"chars": ["^", "^"], "offset": -1},  # Closed eyes
            {"chars": ["*", "*"], "offset": 0}    # Starry eyes
        ]
        selected_eyes = random.choice(eye_styles)
        eye_chars = selected_eyes["chars"]
        eye_offset = selected_eyes["offset"]
        eye_colors = ["blue", "green", "brown", "dark_slate_gray1", "gold1", "violet"]
        eye_color = random.choice(eye_colors)
        self.eye_chars = eye_chars
        self.eye_color = eye_color

        # Left eye
        self.grid[8 + eye_offset][7] = eye_chars[0]
        # Right eye
        self.grid[8 + eye_offset][10] = eye_chars[1]

    def generate_eyebrows(self):
        """Generate and place the eyebrows on the grid."""
        eyebrow_styles = ["▄", "▀", "―", "╌", "︶", "︵", "⌒", "︻", "︼"]
        eyebrow_char = random.choice(eyebrow_styles)
        eyebrow_offset = random.choice([-1, 0])
        eyebrow_color = self.hair_color  # Eyebrows match hair color

        # Left eyebrow
        self.grid[7 + eyebrow_offset][7] = eyebrow_char
        # Right eyebrow
        self.grid[7 + eyebrow_offset][10] = eyebrow_char

    def generate_nose(self):
        """Generate and place the nose on the grid."""
        nose_char = random.choice(["▼", "▾", "∇", "ˇ", "Ƹ", "|", "ʌ"])
        nose_color = self.face_color  # Nose matches face color

        self.grid[9][8] = nose_char
        self.nose_char = nose_char
        self.nose_color = nose_color

    def generate_mouth(self):
        """Generate and place the mouth on the grid."""
        mouth_styles = {
            'smile': ["  ᴖᴖᴖ  "],
            'frown': ["  ᴗᴗᴗ  "],
            'neutral': ["  ───  "],
            'grin': ["  ᕮᕭ  "],
            'surprised': ["   o   "],
            'tongue_out': ["  ᵔᵕᵔ  "],
            'smirk': ["  ◡︵◡ "],
            'kiss': ["   ۳   "],
            'sad': ["  ︵︵︵ "]
        }
        selected_mouth = random.choice(list(mouth_styles.keys()))
        mouth_pattern = mouth_styles[selected_mouth]
        mouth_color = "red3"

        start_row = 11
        for i, line in enumerate(mouth_pattern):
            row = start_row + i
            for j, char in enumerate(line):
                col = 5 + j
                if char != " ":
                    self.grid[row][col] = char

        self.mouth_chars = set(char for line in mouth_pattern for char in line if char.strip())
        self.mouth_color = mouth_color

    def generate_ears(self):
        """Generate and place the ears on the grid."""
        ear_char = random.choice(["(", "<", "[", "{", "ʢ"])
        ear_color = self.face_color  # Ears match face color

        # Left ear
        self.grid[9][5] = ear_char
        # Right ear
        right_ear = ear_char[::-1] if ear_char != "ʢ" else "ʡ"
        self.grid[9][12] = right_ear

    def generate_facial_hair(self):
        """Generate and place optional facial hair on the grid."""
        facial_hair_styles = [
            {"style": "mustache", "pattern": ["  ̴̴̴  "], "offset": 10},
            {"style": "beard", "pattern": [" ██████ "], "offset": 12},
            {"style": "goatee", "pattern": ["   █   "], "offset": 12},
            {"style": "soul_patch", "pattern": ["   ░   "], "offset": 12},
            {"style": "full_beard", "pattern": [" ██████ ", "████████"], "offset": 12},
            {"style": "none", "pattern": [], "offset": 0}
        ]
        selected_style = random.choice(facial_hair_styles)
        facial_hair_pattern = selected_style["pattern"]
        hair_offset = selected_style["offset"]
        facial_hair_color = self.hair_color

        start_row = hair_offset
        for i, line in enumerate(facial_hair_pattern):
            row = start_row + i
            for j, char in enumerate(line):
                col = 5 + j
                if char != " ":
                    self.grid[row][col] = char

        self.facial_hair_chars = set(char for line in facial_hair_pattern for char in line if char.strip())
        self.facial_hair_color = facial_hair_color

    def generate_accessories(self):
        """Generate and place optional accessories on the grid."""
        # Glasses
        if random.choice([True, False]):
            glasses_styles = ["-○-○-", "=○=○=", "◐─◑", "⌐■-■", "ʘ‿ʘ"]
            glasses_char = random.choice(glasses_styles)
            glasses_color = "grey70"

            # Determine the starting column to center the glasses
            glasses_length = len(glasses_char)
            start_col = 9 - glasses_length // 2  # Center the glasses

            # Place the glasses on the grid
            for idx, char in enumerate(glasses_char):
                col = start_col + idx
                self.grid[8][col] = char

            self.glasses_chars = set(glasses_char)
            self.glasses_color = glasses_color
        else:
            self.glasses_chars = set()
            self.glasses_color = None

        # Earrings
        if random.choice([True, False]):
            earring_char = random.choice(["•", "✧", "✦"])
            earring_color = "gold1"

            # Left earring
            self.grid[10][5] = earring_char
            # Right earring
            self.grid[10][12] = earring_char

            self.earring_chars = {earring_char}
            self.earring_color = earring_color
        else:
            self.earring_chars = set()
            self.earring_color = None

        # Nose Piercing
        if random.choice([True, False]):
            piercing_char = random.choice(["¤", "•"])
            piercing_color = "silver"

            self.grid[9][9] = piercing_char  # Place on the nose

            self.piercing_chars = {piercing_char}
            self.piercing_color = piercing_color
        else:
            self.piercing_chars = set()
            self.piercing_color = None

    def grid_to_rich_text(self) -> Text:
        """
        Convert the grid to a Rich Text object with appropriate styling.

        Returns:
            Text: A Rich Text object representing the styled headshot.
        """
        face_text = Text()
        # Only include the relevant rows to eliminate blank space
        start_row = next((i for i, row in enumerate(self.grid) if any(char != " " for char in row)), 0)
        end_row = next((i for i in range(len(self.grid) - 1, -1, -1) if any(char != " " for char in self.grid[i])), len(self.grid) - 1) + 1
        for row in self.grid[start_row:end_row]:
            for char in row:
                style = self.get_style_for_char(char)
                face_text.append(char, style=style)
            face_text.append("\n")
        return face_text

    def get_style_for_char(self, char: str) -> str:
        """Get the style for a given character."""
        if char == "░":  # Face skin
            return self.face_color
        elif char in self.eye_chars:
            return self.eye_color
        elif char == self.nose_char or char in self.piercing_chars:
            return self.nose_color if char == self.nose_char else self.piercing_color
        elif char in self.mouth_chars:
            return self.mouth_color
        elif char in ["▄", "▀", "―", "╌", "︶", "︵", "⌒", "︻", "︼"]:  # Eyebrows
            return self.hair_color
        elif char in ["█", "■", "◆", "@", "▓"]:  # Hair
            return self.hair_color
        elif char in ["(", ")", "<", ">", "[", "]", "{", "}", "ʢ", "ʡ"]:  # Ears
            return self.face_color
        elif char in self.facial_hair_chars:
            return self.facial_hair_color
        elif self.glasses_color and char in self.glasses_chars:
            return self.glasses_color
        elif self.earring_color and char in self.earring_chars:
            return self.earring_color
        else:
            return "black"  # Background

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
