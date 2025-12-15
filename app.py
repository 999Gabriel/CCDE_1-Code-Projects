from flask import Flask, render_template, session, jsonify, request
from model import read_questions, get_rand_question

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_millionaire_game'  # Required for session

# Load questions once at startup
QUESTIONS_FILE = 'millionaire.txt'
questions = read_questions(QUESTIONS_FILE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
@app.route('/game/<int:answer>')
def game(answer=-1):
    # Initialize session if not present
    if 'level' not in session:
        session['level'] = 0
        session['score'] = 0

    current_level = session['level']

    # Check answer if provided
    if answer != -1:
        # Retrieve stored correct answer index from session
        correct_index = session.get('correct_index')

        if correct_index is not None:
            if answer == correct_index:
                # Correct answer
                session['level'] += 1
                session['score'] = session.get('score', 0) + 100 * (session['level']) # Simple scoring
                current_level = session['level']
            else:
                # Wrong answer - Game Over or Reset
                final_score = session['score']
                session.pop('level', None)
                session.pop('score', None)
                session.pop('correct_index', None)
                return render_template('game_over.html', score=final_score)

    # Get a new question for the current level
    # Note: In a real game we might want to persist the question if the user refreshes,
    # but for this exercise we'll just fetch a random one or keep the current one if we haven't answered yet.
    # However, the prompt implies a flow where we answer and get a new one.

    # If we just answered correctly (or started), we need a new question.
    # But if we are just loading the page without an answer (answer=-1), we might want to keep the current question if it exists?
    # The prompt says: "Wichtig ist hier, die aktuelle richtige Position der Antwort in der Session zu merken"

    # Let's simplify: Always get a question for the current level.
    # If we want to prevent cheating by refresh, we would store the current question ID in session.
    # For this exercise, let's just get a random question for the level.

    q = get_rand_question(current_level, questions)

    if not q:
        # No more questions for this level (Win?)
        final_score = session.get('score', 0)
        session.pop('level', None)
        session.pop('score', None)
        return render_template('win.html', score=final_score)

    # Store the correct answer index in session
    # q.answers is shuffled. We need to find where q.correct_answer is.
    correct_index = q.answers.index(q.correct_answer)
    session['correct_index'] = correct_index

    return render_template('game.html', question=q, level=current_level, score=session.get('score', 0))

@app.route('/questions')
def all_questions():
    return render_template('questions.html', questions=questions)

@app.route('/react')
def react_game():
    return render_template('react_game.html')

# --- REST API ---

@app.route('/api/start', methods=['POST'])
def api_start():
    session['level'] = 0
    session['score'] = 0
    return jsonify({'status': 'started', 'level': 0, 'score': 0})

@app.route('/api/question', methods=['GET'])
def api_question():
    if 'level' not in session:
        return jsonify({'error': 'Game not started'}), 400

    current_level = session['level']
    q = get_rand_question(current_level, questions)

    if not q:
        # No more questions (Win)
        return jsonify({'status': 'win', 'score': session.get('score', 0)})

    # Store correct index
    correct_index = q.answers.index(q.correct_answer)
    session['correct_index'] = correct_index

    # Return question data
    return jsonify({
        'text': q.text,
        'answers': q.answers,
        'level': q.level
    })

@app.route('/api/answer', methods=['POST'])
def api_answer():
    if 'level' not in session:
        return jsonify({'error': 'Game not started'}), 400

    data = request.get_json()
    if not data or 'answer_index' not in data:
        return jsonify({'error': 'Missing answer_index'}), 400

    try:
        answer_index = int(data['answer_index'])
    except ValueError:
        return jsonify({'error': 'Invalid answer_index'}), 400

    correct_index = session.get('correct_index')

    if correct_index is None:
         return jsonify({'error': 'No active question'}), 400

    if answer_index == correct_index:
        session['level'] += 1
        session['score'] = session.get('score', 0) + 100 * session['level']
        return jsonify({
            'correct': True,
            'score': session['score'],
            'level': session['level']
        })
    else:
        final_score = session['score']
        session.pop('level', None)
        session.pop('score', None)
        session.pop('correct_index', None)
        return jsonify({
            'correct': False,
            'game_over': True,
            'score': final_score
        })

@app.route('/api/questions', methods=['GET'])
def api_all_questions():
    return jsonify([q.to_dict() for q in questions])

if __name__ == '__main__':
    app.run(debug=True)
