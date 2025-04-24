#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run the Flask app
# python chatbot.py 
python chatbot.py --port=5000
