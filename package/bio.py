import random

class Bio:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Bio: {self.name}"
    
    # function to generate name randomly
    def generate_name(self):
        first_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Helen"]
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    # function to generate profession
    def generate_profession(self):
        professions = ["Engineer", "Doctor", "Scientist", "Pilot", "Teacher", "Artist", "Musician", "Writer"]
        return random.choice(professions)
    
    # function to generate age
    def generate_age(self):
        return random.randint(18, 65)
    
    # function to generate life focus
    def generate_life_focus(self):
        life_focuses = ["Survival", "Wealth", "Happiness", "Fame", "Knowledge", "Love"]
        return random.choice(life_focuses)
    