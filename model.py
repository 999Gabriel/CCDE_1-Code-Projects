from dataclasses import dataclass, field
from typing import List
import random
import csv

@dataclass
class Question:
    id: int
    level: int
    text: str
    correct_answer: str
    wrong_answers: List[str]
    info: str = ""
    answers: List[str] = field(init=False)

    def __post_init__(self):
        # Combine all answers and shuffle them for display, but keep track of correct one
        self.answers = [self.correct_answer] + self.wrong_answers
        random.shuffle(self.answers)

    def to_dict(self):
        return {
            'id': self.id,
            'level': self.level,
            'text': self.text,
            'answers': self.answers,
            'correct_answer': self.correct_answer,
            'info': self.info
        }

def read_questions(fName):
    questions = []
    try:
        with open(fName, 'r', encoding='utf-8') as f:
            # Skip header if it exists or handle it. The file seems to have a header starting with #
            lines = f.readlines()

        question_id = 1
        for line in lines:
            if line.startswith('#') or not line.strip():
                continue

            parts = line.strip().split('\t')
            if len(parts) >= 6:
                level = int(parts[0])
                text = parts[1]
                correct = parts[2]
                wrong = parts[3:6]
                info = parts[6] if len(parts) > 6 else ""

                q = Question(question_id, level, text, correct, wrong, info)
                questions.append(q)
                question_id += 1
    except Exception as e:
        print(f"Error reading file: {e}")

    return questions

def get_rand_question(level, questions):
    level_questions = [q for q in questions if q.level == level]
    if not level_questions:
        return None
    return random.choice(level_questions)
