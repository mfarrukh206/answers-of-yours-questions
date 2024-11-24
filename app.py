from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import openai
import os

# Initialize the Flask app
app = Flask(__name__)

# Set the database configuration to use SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance/history.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration tool
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# GPT API Configuration (replace with your OpenAI API key)
openai.api_key = 'sk-ZT03OqieXfDE1DQQfF_-iYEOsKIxMK2YMNVVDpJik4T3BlbkFJiAeog2LqLnokP8-2segw-XUh6WWHOUFPf0W3jix9UA'

# Define a model for storing questions and answers
class QnA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(2000), nullable=False)


    def __repr__(self):
        return f'QnA(question="{self.question}", answer="{self.answer}")'
    
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def index():
    # Retrieve all question-answer pairs from the database
    history = QnA.query.order_by(QnA.id.desc()).all()  # Orders by most recent
    return render_template('index.html', history=history)

# API route to handle user question and generate AI answer
@app.route('/ask', methods=['POST', 'GET'])
def ask_question():
    data = request.get_json()
    
    # Check if 'question' exists in the incoming data
    if 'question' not in data:
        return jsonify({'error': 'No question provided'}), 400
    
    question = data['question']

    # Call OpenAI GPT-3 API to get an answer
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            max_tokens=150
        )
        answer = response.choices[0].text.strip()
    except Exception as e:
        # Handle any errors from the OpenAI API
        return jsonify({'error': 'OpenAI API error: ' + str(e)}), 500

    # Save the question and answer to the database
    qna = QnA(question=question, answer=answer)
    db.session.add(qna)
    db.session.commit()

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
