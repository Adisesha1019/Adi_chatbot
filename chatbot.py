import random
import spacy
from flask import Flask, render_template, request, jsonify

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to load responses from a text file
def load_responses(file_path):
    responses = {}
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            question = None
            answer = []
            for line in lines:
                line = line.strip()
                if line.startswith("Q:"):
                    if question:
                        responses[question] = "\n".join(answer)
                    question = line.replace("Q: ", "").lower()
                    answer = []
                elif line.startswith("A:"):
                    answer.append(line.replace("A: ", ""))
                else:
                    answer.append(line)
            if question:
                responses[question] = "\n".join(answer)
    except Exception as e:
        print(f"Error loading responses: {e}")
    return responses

# Load responses from the text file
responses = load_responses('responses.txt')

# Function to get a response from the chatbot
def get_response(user_input):
    user_input = user_input.lower()
    user_doc = nlp(user_input)
    best_match = None
    best_score = 0
    for question in responses:
        question_doc = nlp(question)
        score = user_doc.similarity(question_doc)
        if score > best_score:
            best_score = score
            best_match = question
    if best_match and best_score > 0.7:  # Adjust the threshold as needed
        return responses[best_match]
    else:
        return "I'm not sure how to respond to that. I am still in training."

# Create Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    response = get_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
