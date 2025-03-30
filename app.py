import os
import logging
from flask import Flask, render_template, request, jsonify
from chatbot import get_chatbot_response

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

@app.route('/')
def index():
    """Render the main chatbot interface."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint to handle chat requests."""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message.strip():
        return jsonify({'error': 'Empty message'}), 400
    
    try:
        response = get_chatbot_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        logging.error(f"Error generating response: {str(e)}")
        return jsonify({'error': 'Failed to generate response'}), 500

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    logging.error(f"Server error: {str(e)}")
    return jsonify({'error': 'Internal server error'}), 500

# We're using main.py as the entry point for the Replit workflow
