from app import app, db, Question

def run_examples():
    """
    Demonstrates SQLAlchemy operations: Add, Update, Delete.
    """
    print("--- SQLAlchemy ORM Examples ---")

    # We must push an application context to access the database
    with app.app_context():

        # 1. ADD (Create)
        print("\n1. Adding a new question...")
        new_q = Question()
        new_q.level = 1
        new_q.text = "Was ist die Hauptstadt von Pythonia?"
        new_q.correct_answer = "Indentation City"
        new_q.wrong_answers = ["Curly Brace Town", "Semicolon Village", "Parenthesis Park"]
        new_q.info = "Python uses indentation."

        db.session.add(new_q)
        db.session.commit()
        print(f"Added Question: ID={new_q.id}, Text='{new_q.text}'")
        created_id = new_q.id

        # 2. READ (Query)
        print("\n2. Querying the question...")
        q = Question.query.get(created_id)
        if q:
            print(f"Found: {q.text} (Answers: {q.answers})")

        # 3. UPDATE
        print("\n3. Updating the question...")
        if q:
            q.text = "Wo lebt der Python-Erfinder?"
            q.correct_answer = "In den Niederlanden (ursprünglich)"
            # Update wrong answers too
            q.wrong_answers = ["Auf dem Mond", "In einer Schlangengrube", "Im Zoo"]
            db.session.commit()
            print(f"Updated Question: '{q.text}' Correct: '{q.correct_answer}'")

        # Verify Update
        q_updated = Question.query.get(created_id)
        print(f"Verify Update: {q_updated.text}")

        # 4. DELETE
        print("\n4. Deleting the question...")
        if q_updated:
            db.session.delete(q_updated)
            db.session.commit()
            print(f"Deleted Question ID={created_id}")

        # Verify Delete
        q_deleted = Question.query.get(created_id)
        if q_deleted is None:
             print("Verification: Question is gone.")
        else:
             print("Error: Question still exists.")

if __name__ == "__main__":
    run_examples()
