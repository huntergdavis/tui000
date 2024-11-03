# lifemap.py
from textual.widgets import Static
from rich.text import Text

class LifeMap(Static):
    """
    LifeMap widget represents the character's life progression.
    Initially displays a grid where only the first 'X' is colored,
    and all subsequent 'X's are black. With each update, the next
    'X' is colored using the next color from the color list.
    """
    
    def __init__(self, total_elements=240, blocks_per_row=20, **kwargs):
        """
        Initialize the LifeMap.

        Args:
            total_elements (int): Total number of 'X's in the life map.
            blocks_per_row (int): Number of 'X's per row.
            **kwargs: Additional keyword arguments for the Widget.
        """
        super().__init__(**kwargs)
        self.total_elements = total_elements
        self.blocks_per_row = blocks_per_row
        self.rows = self.total_elements // self.blocks_per_row  # e.g., 240 / 20 = 12

        # Initialize the life_map with 'X's
        self.life_map = ["X" for _ in range(self.total_elements)]
        
        # Initialize color_map with 'black' for all 'X's
        self.color_map = ["black" for _ in range(self.total_elements)]
        
        self.current_index = 0  # Tracks the next 'X' to color

        # Initially color the first 'X' if available
        if self.life_map:
            initial_color = "blue"
            self.color_map[0] = initial_color
            self.current_index = 1
            self.refresh()  # Refresh the widget to display the initial color
    
    def increment_progress(self, color: str):
        """
        Color the next 'X' in the life map with the next color from the colors list.
        """
        if self.current_index >= self.total_elements:
            # All 'X's have been colored; optionally, you can reset or stop
            return
        
        # Update the color_map with the new color
        self.color_map[self.current_index] = color
        
        # Increment the current_index for the next update
        self.current_index += 1
        
        # Refresh the widget to display the updated color
        self.refresh()
    
    def reset_progress(self):
        """
        Reset the life map progress, making all 'X's black again.
        """
        # Reset all 'X's to 'black'
        self.color_map = ["black" for _ in range(self.total_elements)]
        
        self.current_index = 0  # Reset the progress index

        # Re-color the first 'X' if available
        if self.life_map:
            initial_color = "blue"
            self.color_map[0] = initial_color
            self.current_index = 1
        
        # Refresh the widget to display the reset state
        self.refresh()
    
    def render(self) -> Text:
        """
        Render the life map as a grid of 'X's.

        Returns:
            Text: The rich Text object representing the life map.
        """
        life_map_text = Text()

        for row in range(self.rows):
            for col in range(self.blocks_per_row):
                index = row * self.blocks_per_row + col
                if index < self.total_elements:
                    x = self.life_map[index]
                    style = self.color_map[index]
                    life_map_text.append(x + " ", style=style)
            life_map_text.append("\n")
        
        return life_map_text
