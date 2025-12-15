import tkinter as tk
from tkinter import messagebox
import requests

API_BASE = "http://127.0.0.1:5000/api"

class MillionaireClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Millionaire Game - Python Client")
        self.root.geometry("600x400")

        self.session = requests.Session()

        # UI Elements
        self.header_frame = tk.Frame(root)
        self.header_frame.pack(pady=10)

        self.level_label = tk.Label(self.header_frame, text="Level: 0", font=("Arial", 12))
        self.level_label.pack(side=tk.LEFT, padx=20)

        self.score_label = tk.Label(self.header_frame, text="Score: 0", font=("Arial", 12))
        self.score_label.pack(side=tk.LEFT, padx=20)

        self.question_label = tk.Label(root, text="Welcome to Millionaire!", font=("Arial", 14), wraplength=500)
        self.question_label.pack(pady=20)

        self.answers_frame = tk.Frame(root)
        self.answers_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.answer_buttons = []
        for i in range(4):
            btn = tk.Button(self.answers_frame, text="", font=("Arial", 12),
                            command=lambda idx=i: self.submit_answer(idx))
            btn.pack(fill=tk.X, padx=50, pady=5)
            self.answer_buttons.append(btn)

        self.start_button = tk.Button(root, text="Start Game", font=("Arial", 14), bg="green", fg="white", command=self.start_game)
        self.start_button.pack(pady=20)

        # Initial State
        self.disable_answers()

    def disable_answers(self):
        for btn in self.answer_buttons:
            btn.config(state=tk.DISABLED, text="")

    def enable_answers(self):
        for btn in self.answer_buttons:
            btn.config(state=tk.NORMAL)

    def start_game(self):
        try:
            response = self.session.post(f"{API_BASE}/start")
            if response.status_code == 200:
                data = response.json()
                self.update_stats(data['level'], data['score'])
                self.start_button.pack_forget()
                self.fetch_question()
            else:
                messagebox.showerror("Error", "Could not start game. Is the server running?")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "Could not connect to server. Make sure app.py is running!")

    def fetch_question(self):
        try:
            response = self.session.get(f"{API_BASE}/question")
            data = response.json()

            if data.get('status') == 'win':
                self.game_over(True, data.get('score'))
                return

            if 'error' in data:
                messagebox.showerror("Error", data['error'])
                return

            self.question_label.config(text=data['text'])
            answers = data['answers']

            for i, btn in enumerate(self.answer_buttons):
                if i < len(answers):
                    btn.config(text=f"{chr(65+i)}. {answers[i]}", state=tk.NORMAL)
                else:
                    btn.config(text="", state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching question: {e}")

    def submit_answer(self, index):
        try:
            response = self.session.post(f"{API_BASE}/answer", json={'answer_index': index})
            data = response.json()

            if data.get('correct'):
                self.update_stats(data['level'], data['score'])
                messagebox.showinfo("Correct!", "That is correct!")
                self.fetch_question()
            elif data.get('game_over'):
                self.game_over(False, data.get('score'))
            else:
                messagebox.showerror("Error", data.get('error', "Unknown error"))

        except Exception as e:
            messagebox.showerror("Error", f"Error submitting answer: {e}")

    def update_stats(self, level, score):
        self.level_label.config(text=f"Level: {level}")
        self.score_label.config(text=f"Score: {score}")

    def game_over(self, win, score):
        title = "Congratulations!" if win else "Game Over"
        msg = f"You won! Final Score: {score}" if win else f"Wrong answer! Final Score: {score}"

        messagebox.showinfo(title, msg)
        self.start_button.pack(pady=20)
        self.start_button.config(text="Play Again")
        self.question_label.config(text=title)
        self.disable_answers()

if __name__ == "__main__":
    root = tk.Tk()
    app = MillionaireClient(root)
    root.mainloop()

