from flask import Flask, request, render_template, jsonify
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Internal server error: {error}')
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            # Validate that form data exists
            if not request.form:
                return jsonify({'error': 'No form data provided'}), 400
            
            # Validate username field
            if 'username' not in request.form:
                return jsonify({'error': 'Username field is required'}), 400
            
            name = request.form['username']
            
            # Validate username is not empty
            if not name or not name.strip():
                return jsonify({'error': 'Username cannot be empty'}), 400
            
            return f"Hello {name}, POST request received"
        
        return render_template('name.html')
    
    except Exception as e:
        logger.error(f'Error in login endpoint: {str(e)}')
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)