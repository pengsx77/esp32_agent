import json
import datetime
import random
import os

class DialogueManager:
    def __init__(self):
        file = os.path.join(os.path.dirname(__file__), "questions.json")
        with open(file, "r", encoding="utf-8") as f:
            self.dialogues = json.load(f)

    def get_today_theme(self):
        week = datetime.date.today().isocalendar()[1]
        theme_index = week % len(self.dialogues)
        theme_name = list(self.dialogues.keys())[theme_index]
        return theme_name, self.dialogues[theme_name]

    def get_daily_questions(self):
        theme, questions = self.get_today_theme()
        return theme, random.sample(questions, min(2, len(questions)))

dialogue_manager = DialogueManager()
