import os
#Fragen aus der Text datei extrahieren und in einer Liste speichern
# ist aufgebaut in #Difficulty	Question	Correct Answer	Answer #2	Answer #3	Answer #4	Background information
def load_questions_from_file(file_path):
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the project root and then to the file
    project_root = os.path.dirname(script_dir)
    full_path = os.path.join(project_root, file_path)

    questions = []
    with open(full_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) >= 7:
                question = {
                    'difficulty': parts[0],
                    'question': parts[1],
                    'correct_answer': parts[2],
                    'answers': parts[2:6],  # includes correct answer and 3 wrong answers
                    'background_info': parts[6]
                }
                questions.append(question)
    return questions
questions = load_questions_from_file('millionaire.txt')
