from flask import Flask, jsonify, request
from flask_cors import CORS
from gemini import configure_gemini, get_gemini_response
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv('api_key.env')
logger.info("Loading environment variables...")

app = Flask(__name__)
CORS(app)

# Configure Gemini with API key
try:
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    configure_gemini(api_key)
    logger.info("Gemini API configured successfully")
except Exception as e:
    logger.error(f"Error configuring Gemini: {str(e)}")
    raise

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Backend is running!"})

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        try:
            data = request.json
            message = data.get('message', '')
            logger.info(f"Received message: {message}")
            
            # Get response from Gemini
            response = get_gemini_response(message)
            logger.info(f"Gemini response: {response}")
            return jsonify(response)
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return jsonify({
                "status": "error",
                "message": f"Server error: {str(e)}"
            }), 500
    
    return jsonify({
        "message": "Hello! Send me a message using POST request.",
        "status": "success"
    })

if __name__ == '__main__':
    logger.info("Starting Flask server on port 5001...")
    app.run(debug=True, host='0.0.0.0', port=5001)
