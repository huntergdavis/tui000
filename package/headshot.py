import random
from rich.text import Text

# Function to center-align a string within a fixed width (18 characters)
def center_text(text: str, width: int = 18) -> str:
    return text.center(width)

# Function to create a blank 18x18 grid
def initialize_grid(size: int = 18) -> list:
    return [[" " for _ in range(size)] for _ in range(size)]

# Function to add an outline to the grid
def add_outline(grid: list) -> None:
    for i in range(18):
        grid[i][0] = "|"
        grid[i][17] = "|"
    for j in range(18):
        grid[0][j] = "-"
        grid[17][j] = "-"

# Function to generate facial features in the grid
def generate_facial_features(grid: list) -> tuple:
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

    return (eye_char, eye_color, nose_char, nose_color, mouth_char, mouth_color, face_fill_char, face_color)

# Function to fill the grid with face background characters
def fill_face(grid: list, face_fill_char: str) -> None:
    for i in range(18):
        for j in range(18):
            if grid[i][j] == " ":
                grid[i][j] = face_fill_char

# Function to convert the grid to a Rich Text object with colors
def grid_to_rich_text(grid: list, eye_char: str, eye_color: str, nose_char: str, nose_color: str, 
                      mouth_char: str, mouth_color: str, face_fill_char: str, face_color: str, 
                      bg_color: str) -> Text:
    face_text = Text()
    for i in range(18):
        for j in range(18):
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

# Function to generate and append the bio information
def generate_bio(name: str, profession: str, age: int, focus: str, face_text: Text) -> None:
    face_text.append(f"\n{center_text(name)}\n", style="bold")
    face_text.append(f"{center_text(profession)}\n", style="italic")
    face_text.append(f"{center_text(f'{age} years old')}\n")
    face_text.append(f"{center_text(focus)}\n", style="bold italic")

# Main function to generate headshot and bio
def generate_headshot_and_bio(name: str, profession: str, age: int, focus: str) -> Text:
    # Initialize the grid
    headshot = initialize_grid()

    # Randomly decide if we're using a background color or an outline
    use_background = random.choice([True, False])

    if not use_background:
        add_outline(headshot)  # Add outline if no background is used

    # Generate facial features and place them in the grid
    (eye_char, eye_color, nose_char, nose_color, mouth_char, mouth_color, face_fill_char, face_color) = generate_facial_features(headshot)

    # Optionally use a background color
    bg_color = random.choice(["on_black", "on_white", "on_grey19", "on_cornsilk1", "on_dark_blue"]) if use_background else ""

    # Fill the face with the background pattern
    fill_face(headshot, face_fill_char)

    # Convert the grid to rich text with coloring
    face_text = grid_to_rich_text(headshot, eye_char, eye_color, nose_char, nose_color, 
                                  mouth_char, mouth_color, face_fill_char, face_color, bg_color)

    # Append bio information below the face
    generate_bio(name, profession, age, focus, face_text)

    return face_text
