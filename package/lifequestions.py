import random
import json
import os

class LifeEventQuestions:

    file_path = "./package/questions.json"


    def __init__(self):
        """
        Initializes the LifeEventQuestions class by loading questions from a JSON file.
        
        Args:
            json_file_path (str): The file path to the JSON file containing questions.
        """
        self.questions = self.load_questions()
    
    def load_questions(self):
        """
        Loads questions from a JSON file.
        
        Args:
            file_path (str): The file path to the JSON file containing questions.
        
        Returns:
            list: A list of question dictionaries.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")
        
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get("questions", [])
    
    def get_random_question(self):
        """Returns a random question and its associated choices."""
        if not self.questions:
            raise ValueError("No questions available to select.")
    
        return random.choice(self.questions)

