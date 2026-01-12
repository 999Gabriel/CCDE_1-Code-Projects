import requests
import json
import pprint


class GameManager:
    """
    Programmatic interface (Client) to manage Millionaire Game questions via REST API.
    Replaces the need for a web-based administration UI.
    """

    def __init__(self, base_url="http://127.0.0.1:5000/api/questions"):
        self.base_url = base_url

    def list_questions(self):
        """Fetches and displays all questions."""
        print(f"\n--- Listing All Questions from {self.base_url} ---")
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            questions = response.json()
            print(f"Total Questions: {len(questions)}")
            for q in questions:
                print(f"[ID: {q['id']}] Level: {q['level']} | {q['text'][:60]}...")
            return questions
        except requests.exceptions.RequestException as e:
            print(f"Error listing questions: {e}")
            return []

    def add_question(self, level, text, correct_answer, wrong_answers, info=""):
        """Adds a new question."""
        print("\n--- Adding New Question ---")
        payload = {
            'level': level,
            'text': text,
            'correct_answer': correct_answer,
            'wrong_answers': wrong_answers,  # List of strings
            'info': info
        }

        try:
            response = requests.post(self.base_url, json=payload)
            if response.status_code == 200:
                created_q = response.json()
                print("Success! Created Question:")
                # pprint.pprint(created_q)
                print(f"ID: {created_q.get('id')} - {created_q.get('text')}")
                return created_q.get('id')
            else:
                print(f"Failed to add question. Status: {response.status_code}")
                print(response.text)
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error adding question: {e}")
            return None

    def update_question(self, question_id, **kwargs):
        """
        Updates an existing question.
        Pass fields to update as keyword arguments (e.g., text="New Text").
        """
        print(f"\n--- Updating Question ID: {question_id} ---")

        # Filter out empty updates
        clean_kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if not clean_kwargs:
            print("No fields provided for update.")
            return

        try:
            url = f"{self.base_url}/{question_id}"
            response = requests.put(url, json=clean_kwargs)

            if response.status_code == 200:
                updated_q = response.json()
                print("Success! Updated Question.")
                return updated_q
            else:
                print(f"Failed to update question. Status: {response.status_code}")
                print(response.text)
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error updating question: {e}")
            return None

    def delete_question(self, question_id):
        """Deletes a question."""
        print(f"\n--- Deleting Question ID: {question_id} ---")
        try:
            url = f"{self.base_url}/{question_id}"
            response = requests.delete(url)

            if response.status_code == 200:
                print(f"Success! {response.json().get('message')}")
                return True
            else:
                print(f"Failed to delete question. Status: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error deleting question: {e}")
            return False


def interactive_menu():
    manager = GameManager()

    while True:
        print("\n=== MILLIONAIRE MANAGER ===")
        print("1. List Questions")
        print("2. Add Question")
        print("3. Delete Question")
        print("4. Update Question (Text change)")
        print("q. Quit")

        choice = input("\nSelect option: ").strip().lower()

        if choice == '1':
            manager.list_questions()

        elif choice == '2':
            try:
                lvl = int(input("Level (1-15): "))
                txt = input("Question text: ")
                corr = input("Correct answer: ")
                print("Enter 3 wrong answers:")
                w1 = input("1: ")
                w2 = input("2: ")
                w3 = input("3: ")
                info = input("Info/Fact: ")

                manager.add_question(level=lvl, text=txt, correct_answer=corr, wrong_answers=[w1, w2, w3], info=info)
            except ValueError:
                print("Error: Level must be a number.")

        elif choice == '3':
            qid = input("Enter Question ID to delete: ")
            if qid:
                manager.delete_question(qid)

        elif choice == '4':
            qid = input("Enter Question ID to update: ")
            new_text = input("Enter new text (leave empty to skip): ")
            if qid and new_text:
                manager.update_question(qid, text=new_text)

        elif choice == 'q':
            print("Bye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    # If run directly, start the interactive menu
    interactive_menu()
