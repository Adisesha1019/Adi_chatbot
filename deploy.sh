#!/bin/bash

# Set environment variables
export FLASK_APP=chatbot.py
export FLASK_ENV=development
export PORT=5000

# Install dependencies
if [ ! -f requirements.txt ]; then
  echo "requirements.txt not found!"
  exit 1
fi
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Verify spaCy model download
if ! python -m spacy validate; then
  echo "spaCy model download failed!"
  exit 1
fi

# Run the Flask app
# python chatbot.py --port=5000
