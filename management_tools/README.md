# Millionaire Game Management Tools

This directory contains tools for managing the content and state of the Flask Millionaire Game.

## Prerequisites

Ensure the game server is running:

```bash
# In the project root
python app.py
```

## Tools

### 1. Game Manager (`manage_game.py`)
A command-line script to programmatically Add, Edit, List, and Delete questions via the REST API.

**Usage:**
```bash
python manage_game.py
```

It acts as a "Code UI" to administer the game without a web interface.

### 2. Verify API (`verify_api.py`)
A script to test the REST API endpoints and ensure the backend is functioning correctly.

**Usage:**
```bash
python verify_api.py
```

## Notes
- These tools require the `requests` library (`pip install requests`).
- They communicate with `http://127.0.0.1:5000/api/questions`.

