from flask_sqlalchemy import SQLAlchemy
import random

db = SQLAlchemy()

class Question(db.Model):
    __tablename__ = 'millionaire'

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column('difficulty', db.Integer)
    text = db.Column('question', db.Text)
    correct_answer = db.Column(db.Text)
    answer2 = db.Column(db.Text)
    answer3 = db.Column(db.Text)
    answer4 = db.Column(db.Text)
    info = db.Column('background_information', db.Text)

    def __repr__(self):
        return f'<Question {self.id}: {self.text}>'

    @property
    def wrong_answers(self):
        return [self.answer2, self.answer3, self.answer4]

    @wrong_answers.setter
    def wrong_answers(self, value):
        if len(value) >= 1: self.answer2 = value[0]
        if len(value) >= 2: self.answer3 = value[1]
        if len(value) >= 3: self.answer4 = value[2]

    @property
    def answers(self):
        # Cache shuffled answers on the instance so it stays consistent during the request
        if not hasattr(self, '_shuffled_answers'):
            opts = [self.correct_answer, self.answer2, self.answer3, self.answer4]
            # Filter out None values just in case
            opts = [o for o in opts if o]
            random.shuffle(opts)
            self._shuffled_answers = opts
        return self._shuffled_answers

    def to_dict(self):
        return {
            'id': self.id,
            'level': self.level,
            'text': self.text,
            'answers': self.answers,
            'correct_answer': self.correct_answer,
            'info': self.info
        }

def get_rand_question(level, questions_query=None):
    # questions_query is now ignored, we use DB
    # We want a random question of a certain level
    # SQLite random ordering: order_by(func.random())
    from sqlalchemy.sql.expression import func
    return Question.query.filter_by(level=level).order_by(func.random()).first()

