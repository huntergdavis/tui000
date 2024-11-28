# character.py

from datetime import datetime
import os
from package.bio import Bio
from rich.text import Text
import random
import json
from typing import List, Dict, Optional, Set, Tuple


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
        self.generate_accessories()  # Glasses, earrings, piercings, hats

        # Convert the grid to rich text with coloring
        self.headshot_text = self.grid_to_rich_text()

        # Cache the headshot without bio by making a deep copy
        self.headshot_text_cache = self.headshot_text.copy()

        # Append bio information below the face
        self.generate_bio(self.headshot_text)

    def generate_face_shape(self):
        """Define the face shape in the grid."""
        face_char = "░"  # Light shade block for skin
        self.face_color = random.choice([
            "light_yellow", "light_salmon1", "wheat1", "navajo_white1",
            "bisque1", "misty_rose1", "rosy_brown1", "sandy_brown",
            "peach_puff1", "goldenrod1"
        ])

        self.face_start_row = 4  # Store the face's starting row for alignment

        # Define face boundaries (ellipse shape)
        for row in range(self.face_start_row, 14):
            for col in range(5, 13):
                if (row - 9) ** 2 + (col - 9) ** 2 <= 16:  # Circle equation
                    self.grid[row][col] = face_char

    def generate_hairstyle(self):
        """Generate and place the hairstyle on the grid."""
        hairstyles = self.get_hairstyles()
        selected_hairstyle = random.choice(hairstyles)
        hair_pattern = selected_hairstyle["pattern"]
        hair_offset = selected_hairstyle["offset"]
        self.hair_color = random.choice([
            "brown", "dark_red", "yellow", "grey69", "black", "light_blue",
            "purple", "green", "pink", "cyan", "red", "magenta", "orange1",
            "dark_goldenrod", "dark_orange", "orchid", "deep_pink3", "turquoise2",
            "spring_green2", "light_sea_green"
        ])

        start_row = self.face_start_row + hair_offset
        self.place_pattern_on_grid(hair_pattern, start_row, 5)

    def generate_eyes(self):
        """Generate and place the eyes on the grid."""
        eye_styles = self.get_eye_styles()
        selected_eyes = random.choice(eye_styles)
        eye_chars = selected_eyes["chars"]
        eye_offset = selected_eyes["offset"]
        self.eye_color = random.choice([
            "blue", "green", "brown", "dark_slate_gray1", "gold1", "violet",
            "steel_blue1", "aquamarine1", "chartreuse1", "deep_pink1",
            "light_coral", "orange_red1", "yellow1"
        ])
        self.eye_chars = set(eye_chars)

        # Left eye
        self.grid[8 + eye_offset][7] = eye_chars[0]
        # Right eye
        self.grid[8 + eye_offset][10] = eye_chars[1]

    def generate_eyebrows(self):
        """Generate and place the eyebrows on the grid."""
        eyebrow_char = random.choice(self.get_eyebrow_styles())
        eyebrow_offset = random.choice([-1, 0])
        self.eyebrow_color = self.hair_color  # Eyebrows match hair color

        # Left eyebrow
        self.grid[7 + eyebrow_offset][7] = eyebrow_char
        # Right eyebrow
        self.grid[7 + eyebrow_offset][10] = eyebrow_char

    def generate_nose(self):
        """Generate and place the nose on the grid."""
        nose_char = random.choice(self.get_nose_styles())
        self.nose_color = self.face_color  # Nose matches face color
        self.nose_char = nose_char

        self.grid[9][8] = nose_char

    def generate_mouth(self):
        """Generate and place the mouth on the grid."""
        mouth_styles = self.get_mouth_styles()
        selected_mouth = random.choice(mouth_styles)
        mouth_pattern = selected_mouth["pattern"]
        self.mouth_color = "red3"
        self.mouth_chars = set(char for line in mouth_pattern for char in line if char.strip())

        start_row = 11
        self.place_pattern_on_grid(mouth_pattern, start_row, 5)

    def generate_ears(self):
        """Generate and place the ears on the grid."""
        ear_char = random.choice(self.get_ear_styles())
        self.ear_color = self.face_color  # Ears match face color

        # Left ear
        self.grid[9][5] = ear_char
        # Right ear
        right_ear = self.get_mirrored_char(ear_char)
        self.grid[9][12] = right_ear

    def generate_facial_hair(self):
        """Generate and place optional facial hair on the grid."""
        facial_hair_styles = self.get_facial_hair_styles()
        selected_style = random.choice(facial_hair_styles)
        facial_hair_pattern = selected_style["pattern"]
        hair_offset = selected_style["offset"]
        self.facial_hair_color = self.hair_color
        self.facial_hair_chars = set(char for line in facial_hair_pattern for char in line if char.strip())

        start_row = hair_offset
        self.place_pattern_on_grid(facial_hair_pattern, start_row, 5)

    def generate_accessories(self):
        """Generate and place optional accessories on the grid."""
        self.glasses_chars = set()
        self.glasses_color = None
        self.earring_chars = set()
        self.earring_color = None
        self.piercing_chars = set()
        self.piercing_color = None
        self.hat_chars = set()
        self.hat_color = None

        # Glasses
        if random.choice([True, False]):
            glasses_styles = self.get_glasses_styles()
            glasses_char = random.choice(glasses_styles)
            self.glasses_color = random.choice([
                "grey70", "gold1", "silver", "steel_blue1", "dark_red",
                "dark_green", "navy_blue", "purple", "deep_sky_blue1"
            ])
            self.glasses_chars = set(glasses_char)
            self.place_centered_pattern(glasses_char, 8)

        # Earrings
        if random.choice([True, False]):
            earring_char = random.choice(["•", "✧", "✦", "❖", "♦", "♢"])
            self.earring_color = random.choice([
                "gold1", "silver", "orchid", "deep_pink1", "turquoise2"
            ])
            self.earring_chars = {earring_char}

            # Left earring
            self.grid[10][5] = earring_char
            # Right earring
            self.grid[10][12] = earring_char

        # Nose Piercing
        if random.choice([True, False]):
            piercing_char = random.choice(["¤", "•", "✪", "✩"])
            self.piercing_color = random.choice(["silver", "gold1", "cyan", "magenta"])
            self.piercing_chars = {piercing_char}

            self.grid[9][9] = piercing_char  # Place on the nose

        # Hat
        if random.choice([True, False]):
            hat_styles = self.get_hat_styles()
            selected_hat = random.choice(hat_styles)
            hat_pattern = selected_hat["pattern"]
            hat_offset = selected_hat["offset"]
            self.hat_color = random.choice([
                "red", "green", "blue", "yellow", "magenta", "cyan",
                "white", "grey70", "purple", "orange1", "dark_orange",
                "navy_blue", "dark_red", "spring_green1", "light_pink1"
            ])
            self.hat_chars = set(char for line in hat_pattern for char in line if char.strip())

            # Adjust hat starting row to align properly with the face
            start_row = self.face_start_row + hat_offset +1
            self.place_pattern_on_grid(hat_pattern, start_row, 5)

    def place_pattern_on_grid(self, pattern: List[str], start_row: int, start_col: int) -> None:
        """Place a pattern on the grid starting from the specified row and column."""
        for i, line in enumerate(pattern):
            row = start_row + i
            for j, char in enumerate(line):
                col = start_col + j
                if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
                    if char != " ":
                        self.grid[row][col] = char

    def place_centered_pattern(self, pattern: str, row: int) -> None:
        """Place a pattern centered horizontally on the grid at the specified row."""
        pattern_length = len(pattern)
        start_col = (len(self.grid[0]) - pattern_length) // 2
        for idx, char in enumerate(pattern):
            col = start_col + idx
            if 0 <= col < len(self.grid[0]):
                self.grid[row][col] = char

    def grid_to_rich_text(self) -> Text:
        """
        Convert the grid to a Rich Text object with appropriate styling.

        Returns:
            Text: A Rich Text object representing the styled headshot.
        """
        face_text = Text()
        # Only include the relevant rows to eliminate blank space
        start_row = next((i for i, row in enumerate(self.grid) if any(char != " " for char in row)), 0)
        end_row = next((i for i in range(len(self.grid) - 1, -1, -1)
                        if any(char != " " for char in self.grid[i])), len(self.grid) - 1) + 1
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
        elif char in self.get_eyebrow_styles():
            return self.eyebrow_color
        elif char in self.hair_characters():
            return self.hair_color
        elif char in self.get_ear_styles():
            return self.ear_color
        elif char in self.facial_hair_chars:
            return self.facial_hair_color
        elif self.glasses_color and char in self.glasses_chars:
            return self.glasses_color
        elif self.earring_color and char in self.earring_chars:
            return self.earring_color
        elif self.hat_color and char in self.hat_chars:
            return self.hat_color
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

    # Helper methods to provide data for variations
    def get_hairstyles(self) -> List[Dict]:
        """Return a list of hairstyle variations."""
        base_patterns = [
            {"style": "short", "pattern": [" ██████ ", "████████"], "offset": -2},
            {"style": "medium", "pattern": ["  ████  ", " ██████ ", "████████"], "offset": -3},
            {"style": "long", "pattern": ["   ██   ", "  ████  ", " ██████ ", "████████"], "offset": -4},
            {"style": "curly", "pattern": ["  @@@@  ", " @@@@@@ ", "@@@@@@@@"], "offset": -3},
            {"style": "afro", "pattern": ["  ▓▓▓▓  ", " ▓▓▓▓▓▓ ", "▓▓▓▓▓▓▓▓"], "offset": -3},
            {"style": "ponytail", "pattern": ["   ██   ", "  ████  ", "   ██   ", "   ██   "], "offset": -4},
            {"style": "mohawk", "pattern": ["    █   ", "    █   ", "    █   ", "    █   "], "offset": -4},
            {"style": "braids", "pattern": ["  ██ ██ ", " ██ ██ ██", "██ ██ ██"], "offset": -3},
            {"style": "wavy", "pattern": ["  ≋≋≋≋  ", " ≋≋≋≋≋≋ ", "≋≋≋≋≋≋≋≋"], "offset": -3},
            {"style": "spiky", "pattern": [r"  /\/\/\  ", r" /\/\/\/\ ", r"/\/\/\/\/\\"], "offset": -3},
            # Additional patterns can be added here
        ]
        return base_patterns

    def hair_characters(self) -> Set[str]:
        """Return a set of characters used in hairstyles."""
        chars = set()
        for style in self.get_hairstyles():
            for line in style["pattern"]:
                chars.update(set(line))
        return chars - {" "}  # Exclude spaces

    def get_eye_styles(self) -> List[Dict]:
        """Return a list of eye variations."""
        return [
            {"chars": ["●", "●"], "offset": 0},
            {"chars": ["◕", "◕"], "offset": 0},
            {"chars": ["⊙", "⊙"], "offset": 0},
            {"chars": ["^", "^"], "offset": -1},
            {"chars": ["*", "*"], "offset": 0},
            {"chars": ["-", "-"], "offset": -1},
            {"chars": ["o", "o"], "offset": 0},
            {"chars": ["O", "O"], "offset": 0},
            {"chars": ["•", "•"], "offset": 0},
            {"chars": ["x", "x"], "offset": 0},
            {"chars": ["@", "@"], "offset": 0},
            {"chars": ["0", "0"], "offset": 0},
            {"chars": ["ʘ", "ʘ"], "offset": 0},
            # Additional eye styles can be added here
        ]

    def get_eyebrow_styles(self) -> List[str]:
        """Return a list of eyebrow variations."""
        return ["▄", "▀", "―", "╌", "︶", "︵", "⌒", "︻", "︼", "=", "≡", "≋", "~", "^", "ˇ", "￣", "﹀"]

    def get_nose_styles(self) -> List[str]:
        """Return a list of nose variations."""
        return ["▼", "▾", "∇", "ˇ", "Ƹ", "|", "ʌ", "v", ">", "<", "⊃", "⊂", "=", ":", "-", "_", "ʖ"]

    def get_mouth_styles(self) -> List[Dict]:
        """Return a list of mouth variations."""
        base_patterns = [
            {"pattern": ["  ᴖᴖᴖ  "]},
            {"pattern": ["  ᴗᴗᴗ  "]},
            {"pattern": ["  ───  "]},
            {"pattern": ["  ᕮᕭ  "]},
            {"pattern": ["   o   "]},
            {"pattern": ["  ᵔᵕᵔ  "]},
            {"pattern": ["  ◡︵◡ "]},
            {"pattern": ["   ۳   "]},
            {"pattern": ["  ︵︵︵ "]},
            {"pattern": ["  ωωω  "]},
            {"pattern": ["  ▽▽▽  "]},
            {"pattern": ["  ∩∩∩  "]},
            {"pattern": ["  ∪∪∪  "]},
            {"pattern": ["  ∞∞∞  "]},
            # Additional mouth styles can be added here
        ]
        return base_patterns

    def get_ear_styles(self) -> List[str]:
        """Return a list of ear variations."""
        return ["(", "<", "[", "{", "ʢ", "|", "/", "\\", "«", "‹"]

    def get_facial_hair_styles(self) -> List[Dict]:
        """Return a list of facial hair variations."""
        base_patterns = [
            {"style": "mustache", "pattern": ["  ̴̴̴  "], "offset": 10},
            {"style": "beard", "pattern": [" ██████ "], "offset": 12},
            {"style": "goatee", "pattern": ["   █   "], "offset": 12},
            {"style": "soul_patch", "pattern": ["   ░   "], "offset": 12},
            {"style": "full_beard", "pattern": [" ██████ ", "████████"], "offset": 12},
            {"style": "chin_strap", "pattern": [" █     █ "], "offset": 12},
            {"style": "mutton_chops", "pattern": ["█       █"], "offset": 12},
            {"style": "stubble", "pattern": [" ░░░░░░ "], "offset": 12},
            {"style": "handlebar", "pattern": [" ╭━━━╮ "], "offset": 10},
            {"style": "horseshoe", "pattern": [" █     █ "], "offset": 10},
            {"style": "none", "pattern": [], "offset": 0}
            # Additional facial hair styles can be added here
        ]
        return base_patterns

    def get_glasses_styles(self) -> List[str]:
        """Return a list of glasses variations."""
        return ["-○-○-", "=○=○=", "◐─◑", "⌐■-■", "ʘ‿ʘ", "ᴑ---ᴑ", "¤---¤", "c⌣⊂", "⊃⌣⊂", "༼༗", "✿‿✿"]

    def get_hat_styles(self) -> List[Dict]:
        """Return a list of hat variations."""
        base_patterns = [
            {"style": "top_hat", "pattern": ["  ██████ ", "  ██████ "], "offset": -2},
            {"style": "beanie", "pattern": ["  ▒▒▒▒▒▒ "], "offset": -1},
            {"style": "cowboy", "pattern": [" ████████"], "offset": -1},
            {"style": "beret", "pattern": ["   ███   "], "offset": -1},
            {"style": "cap", "pattern": [" ██████  "], "offset": -1},
            {"style": "fedora", "pattern": [" ███████ "], "offset": -1},
            {"style": "wizard", "pattern": ["    /\\   ", "   /  \\  ", "  /____\\ "], "offset": -3},
            {"style": "crown", "pattern": ["  👑👑👑  "], "offset": -1},
            {"style": "turban", "pattern": ["  ≈≈≈≈≈≈ "], "offset": -1},
            {"style": "flower", "pattern": ["   ✿✿✿   "], "offset": -1},
            # Additional hat styles can be added here
        ]
        return base_patterns

    def get_mirrored_char(self, char: str) -> str:
        """Return the mirrored version of a character if possible."""
        mirror_map = {"(": ")", "<": ">", "[": "]", "{": "}", "ʢ": "ʡ", "/": "\\", "\\": "/",
                      "«": "»", "‹": "›"}
        return mirror_map.get(char, char)

