from package.character import Character
import random

class LifeEvents:
    def __init__(self):
        pass

    def checkforlifeevent(self, character: Character) -> str:
        """
        Determines whether a life event occurs for the character based on their age and probability.

        Args:
            character (Character): The character instance whose life event is being checked.

        Returns:
            str: "death" if a fatal life event occurs, otherwise "life".
        """
        age = character.bio.age
        death_probability = 0.0  # Initialize death probability

        # Define death probability based on age brackets
        if age < 60:
            death_probability = 0.01  # 1% chance of death
        elif 60 <= age < 80:
            # Linear increase from 1% at age 60 to 50% at age 80
            death_probability = 0.01 + ((age - 60) / 20) * (0.50 - 0.01)
        elif 80 <= age < 100:
            # Linear increase from 50% at age 80 to 100% at age 100
            death_probability = 0.50 + ((age - 80) / 20) * (1.00 - 0.50)
        else:
            death_probability = 1.00  # 100% chance of death at age 100+

        # Generate a random float between 0 and 1
        random_value = random.random()

        # Determine the life event based on death probability
        if random_value < death_probability:
            return "death"
        else:
            return "life"
