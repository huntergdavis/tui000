

# Function for generating the headshot in the corner (9x9 box)
def generate_headshot() -> str:
    return "\n".join([
        "  .   .  ",
        "   \\ /   ",
        "    X    ",
        "   / \\   ",
        "  '   '  ",
    ])