# character.py
from package.bio import Bio

class Character:
    def __init__(self):
        self.refresh()  # Initialize by refreshing character data

    def initialize_life_map_data(self):
        # Initialize a 50x60 grid of 'X's
        return [['X' for _ in range(60)] for _ in range(50)]

    def update_life_map_data(self, new_data):
        """Update the life map data."""
        self.life_map_data = new_data

    def refresh(self):
        """Refresh the character's data."""
        self.bio = Bio()  # Re-generate bio data
        self.life_map_data = self.initialize_life_map_data()  # Reset life map data
