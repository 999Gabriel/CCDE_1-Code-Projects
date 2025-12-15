#main file for who wants to be a millionare
import random
from model import questions
from model.questions import load_questions_from_file

path = 'millionaire.txt'

questions = load_questions_from_file(path)

def ask_question(question):
    print("\nQuestion:")
    print(question['question'])
    answers = question['answers']
    random.shuffle(answers)
    for idx, answer in enumerate(answers, 1):
        print(f"{idx}. {answer}")
    return answers
def get_user_answer():
    while True:
        try:
            choice = int(input("Your answer (1-4): "))
            if 1 <= choice <= 4:
                return choice
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")
def main():
    score = 0
    random.shuffle(questions)
    for question in questions:
        answers = ask_question(question)
        user_choice = get_user_answer()
        selected_answer = answers[user_choice - 1]
        if selected_answer == question['correct_answer']:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was: {question['correct_answer']}")
        print(f"Background info: {question['background_info']}")
    print(f"\nGame over! Your final score is: {score}/{len(questions)}")
if __name__ == "__main__":
    main()# Compare this snippet from src/main.py: