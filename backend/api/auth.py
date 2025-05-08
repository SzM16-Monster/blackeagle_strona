from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user
import logging

auth_bp = Blueprint('auth', __name__)

# Configure logging
logging.basicConfig(
    filename='import.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        raw_data = request.get_data(as_text=True)
        logging.info(f"Raw request data: {raw_data}")
        data = request.get_json()
        logging.info(f"Parsed JSON: {data}")
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not all([email, username, password]):
            logging.warning('Registration failed: missing required fields')
            return jsonify({'error': 'Missing required fields (email, username, password)'}), 400

        user = register_user(first_name, last_name, email, username, password)
        if user:
            return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201
        return jsonify({'error': 'Username or email already exists'}), 400
    except Exception as e:
        logging.error(f"Error in register: {str(e)}")
        return jsonify({'error': f"Internal server error: {str(e)}"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        raw_data = request.get_data(as_text=True)
        logging.info(f"Raw request data: {raw_data}")
        data = request.get_json()
        logging.info(f"Parsed JSON: {data}")
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            logging.warning('Login failed: missing required fields')
            return jsonify({'error': 'Missing required fields'}), 400

        token = login_user(email, password)
        if token:
            return jsonify({'token': token}), 200
        return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        logging.error(f"Error in login: {str(e)}")
        return jsonify({'error': f"Internal server error: {str(e)}"}), 500