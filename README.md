# Flask Millionaire 💰

A RESTful implementation of the classic "Who Wants to Be a Millionaire" game, featuring a Flask backend, a text-based Node.js client, and programmatic management tools.

## 🚀 Features

*   **REST API Backend**: Powered by Flask & Flask-RESTful.
*   **Game Logic**: Levels, scoring, and randomized questions.
*   **In-Memory State**: Fast and simple state management (session-based).
*   **Management CLI**: specialized Python script to Add, Update, and Delete questions via API.
*   **Multiple Clients**:
    *   **Node.js TUI**: A beautiful terminal-based interface using ANSI colors.
    *   **Python GUI**: A lightweight Tkinter client.
    *   **Web Interface**: (Classic Jinja2 templates included).

## 🛠️ Installation

### Prerequisites
*   Python 3.12+
*   Node.js v18+ (for the TUI client)

### Setup
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/flask_millionaire.git
    cd flask_millionaire
    ```

2.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🎮 How to Run

### 1. Start the Game Server
The backend must be running for any client or tool to work.

```bash
python app.py
```
*   Server runs at: `http://127.0.0.1:5000`

### 2. Manage Content (Admin) 🛠️
Use the interactive management tool to add or edit questions without touching the database file.

```bash
python management_tools/manage_game.py
```
*   Follow the on-screen menu to List, Add, Update, or Delete questions.

### 3. Play the Game 🎲

#### Option A: Node.js Terminal Client (Recommended)
An immersive text-based experience.
```bash
node game_clients/client_node.js
```

#### Option B: Python Client
```bash
python game_clients/client_gui.py
```

#### Option C: Web Browser
Visit `http://127.0.0.1:5000` in your browser.

## 📂 Project Structure

*   `app.py`: Main Flask application entry point.
*   `model.py`: Data models and question loader.
*   `millionaire.txt`: Flat-file database of initial questions.
*   `management_tools/`: Admin scripts (`manage_game.py`, `verify_api.py`).
*   `game_clients/`: Player applications (`client_node.js`, `client_gui.py`).
*   `templates/`: HTML templates for the web view.

## 🔌 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/questions` | List all questions |
| `POST` | `/api/questions` | Add a new question |
| `PUT` | `/api/questions/<id>` | Update a question |
| `DELETE` | `/api/questions/<id>` | Delete a question |
| `POST` | `/api/start` | Start a new game session |
| `GET` | `/api/question` | Get current random question |
| `POST` | `/api/answer` | Submit an answer |

## 📝 License

This project is for educational purposes.

