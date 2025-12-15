import random
import csv

class Question:
    def __init__(self, level, text, correct_answer, wrong_answers, info=""):
        self.level = int(level)
        self.text = text
        self.correct_answer = correct_answer
        self.wrong_answers = wrong_answers
        self.info = info

        # Combine all answers and shuffle them for display, but keep track of correct one
        self.answers = [correct_answer] + wrong_answers
        random.shuffle(self.answers)

    def to_dict(self):
        return {
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

        for line in lines:
            if line.startswith('#') or not line.strip():
                continue

            parts = line.strip().split('\t')
            if len(parts) >= 6:
                level = parts[0]
                text = parts[1]
                correct = parts[2]
                wrong = parts[3:6]
                info = parts[6] if len(parts) > 6 else ""

                q = Question(level, text, correct, wrong, info)
                questions.append(q)
    except Exception as e:
        print(f"Error reading file: {e}")

    return questions

def get_rand_question(level, questions):
    level_questions = [q for q in questions if q.level == level]
    if not level_questions:
        return None
    return random.choice(level_questions)

