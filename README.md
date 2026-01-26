# Flask Millionaire 💰

A RESTful implementation of the classic "Who Wants to Be a Millionaire" game, featuring a Flask backend, SQLAlchemy database integration, and programmatic management tools.

## 🚀 Features

*   **REST API Backend**: Powered by Flask & Flask-RESTful.
*   **Database Integration**: Uses **SQLAlchemy** with a **SQLite** database (`millionaire.sqlite3`) instead of flat files.
*   **Game Logic**: Levels, scoring, and randomized questions fetched via SQL queries.
*   **Programmatic Access**: Python script demonstrating CRUD operations via ORM.
*   **Clients**:
    *   **Web Interface**: Integrated browser-based game using Jinja2 templates.
    *   **REST Clients**: API endpoints available for external tools.

## 🛠️ Installation

### Prerequisites
*   Python 3.12+

### Setup
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/999Gabriel/CCDE_1-Code-Projects.git
    cd "SQLAlchemy Millionaire"
    ```

2.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Database Setup**:
    *   The project requires the `millionaire.sqlite3` file in the root directory.
    *   (Optional) You can inspect the database using tools like *DB Browser for SQLite* or `termsql`.

## 🎮 How to Run

### 1. Start the Game Server
The backend must be running for the web interface and API to work.

```bash
python app.py
```
*   Server runs at: `http://127.0.0.1:5000`
*   Open your browser to this address to play the game.

### 2. Database Examples (Admin/Dev) 🛠️
Use the example script to see how to Add, Update, and Delete questions using SQLAlchemy ORM (Requirement 3c).

```bash
python sqlalchemy_examples.py
```
*   This script acts as a demonstration of programmatic database manipulation without using raw SQL.

## 📂 Project Structure

*   `app.py`: Main Flask application entry point with REST API and Route configuration.
*   `model.py`: SQLAlchemy database models (`Question` class) and helper functions.
*   `millionaire.sqlite3`: The SQLite database file.
*   `sqlalchemy_examples.py`: Script demonstrating CRUD operations on the database.
*   `templates/`: HTML templates for the web view.
*   `requirements.txt`: List of Python dependencies.

## 🔌 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/questions` | List all questions from DB |
| `POST` | `/api/questions` | Add a new question to DB |
| `PUT` | `/api/questions/<id>` | Update a question in DB |
| `DELETE` | `/api/questions/<id>` | Delete a question from DB |
| `GET` | `/api/question` | Get a random question (SQL-optimized) |

## 📝 License

This project is for educational purposes (School Exercise 07).
