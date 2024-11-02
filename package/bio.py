import random

class Bio:
    def __init__(self):
        self.name = self.generate_name()
        self.profession = self.generate_profession()
        self.age = self.generate_age()
        self.life_focus = self.generate_life_focus()

    @staticmethod
    def generate_name():
        first_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Helen"]
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    @staticmethod
    def generate_profession():
        professions = ["Engineer", "Doctor", "Scientist", "Pilot", "Teacher", "Artist", "Musician", "Writer"]
        return random.choice(professions)
    
    @staticmethod
    def generate_age():
        return random.randint(18, 65)
    
    @staticmethod
    def generate_life_focus():
        life_focuses = ["Survival", "Wealth", "Happiness", "Fame", "Knowledge", "Love"]
        return random.choice(life_focuses)
