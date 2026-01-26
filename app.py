from flask import Flask, render_template, session, jsonify, request
from flask_restful import Resource, Api, reqparse
from model import get_rand_question, Question, db
import os

app = Flask(__name__)
api = Api(app)
app.secret_key = 'super_secret_key_for_millionaire_game'  # Required for session

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'millionaire.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# questions = read_questions(QUESTIONS_FILE) REMOVED


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


    # Get a random question for the current level
    q = get_rand_question(current_level)

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
    questions = Question.query.all()
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
    q = get_rand_question(current_level)

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
    questions = Question.query.all()
    return jsonify([q.to_dict() for q in questions])

# --- API Resources ---

class QuestionResource(Resource):
    def get(self, question_id):
        question = Question.query.get(question_id)
        if question:
            return jsonify(question.to_dict())
        return {'message': 'Question not found'}, 404

    def delete(self, question_id):
        question = Question.query.get(question_id)
        if question:
            db.session.delete(question)
            db.session.commit()
            return {'message': 'Question deleted'}
        return {'message': 'Question not found'}, 404

    def put(self, question_id):
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400

        question = Question.query.get(question_id)
        if not question:
            return {'message': 'Question not found'}, 404

        if 'level' in data:
            question.level = int(data['level'])
        if 'text' in data:
            question.text = data['text']
        if 'info' in data:
            question.info = data.get('info', "")

        if 'correct_answer' in data:
            question.correct_answer = data['correct_answer']
            # Removing cached shuffled list so it regenerates on next access
            if hasattr(question, '_shuffled_answers'):
                del question._shuffled_answers

        if 'wrong_answers' in data:
            # Setter handles mapping to answer2, answer3, answer4
            question.wrong_answers = data['wrong_answers']
            if hasattr(question, '_shuffled_answers'):
                del question._shuffled_answers

        db.session.commit()
        return jsonify(question.to_dict())


class QuestionsListResource(Resource):
    def get(self):
        questions = Question.query.all()
        return jsonify([q.to_dict() for q in questions])

    def post(self):
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400

        # Basic validation
        required_fields = ['level', 'text', 'correct_answer', 'wrong_answers']
        for field in required_fields:
            if field not in data:
                return {'message': f'Missing field: {field}'}, 400

        new_question = Question()
        new_question.level = int(data['level'])
        new_question.text = data['text']
        new_question.correct_answer = data['correct_answer']
        new_question.wrong_answers = data['wrong_answers'] # Uses setter
        new_question.info = data.get('info', "")

        # ID is auto-increment usually, let DB handle it

        db.session.add(new_question)
        db.session.commit()

        return jsonify(new_question.to_dict())


class QuestionSearchResource(Resource):
    def get(self, query):
        # ILIKE is not standard in SQLite but SQLAlchemy emulates or we use logic.
        # For simplicity let's use contains.
        search = f"%{query}%"
        # Search in text or any of the answers.
        # It's complex to search in all answer columns in one go cleanly OR logic.
        from sqlalchemy import or_
        results = Question.query.filter(
            or_(
                Question.text.like(search),
                Question.correct_answer.like(search),
                Question.answer2.like(search),
                Question.answer3.like(search),
                Question.answer4.like(search)
            )
        ).all()

        return jsonify([q.to_dict() for q in results])

# Register Resources
api.add_resource(QuestionResource, '/api/questions/<int:question_id>')
api.add_resource(QuestionsListResource, '/api/questions')
api.add_resource(QuestionSearchResource, '/api/questions/search/<string:query>')


@app.route('/game_random_question')
def game_random_question():
    level = request.args.get('level', default=1, type=int)
    question = get_rand_question(level)
    if question:
        return jsonify(question.to_dict())
    return jsonify({'message': 'No question found for this level'}), 404

if __name__ == '__main__':
    app.run(debug=True)
