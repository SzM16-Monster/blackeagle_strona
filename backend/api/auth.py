from flask import Blueprint, request, jsonify
from services.auth_service import get_user_watched_movies, register_user, login_user, decode_jwt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import decode_token
import logging
import redis

auth_bp = Blueprint('auth', __name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

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

           user = login_user(email, password)
           if user:
               access_token = create_access_token(identity=user.id)
               return jsonify({'token': access_token}), 200
           return jsonify({'error': 'Invalid email or password'}), 401
       except Exception as e:
           logging.error(f"Error in login: {str(e)}")
           return jsonify({'error': f"Internal server error: {str(e)}"}), 500

@auth_bp.route('/user/movies', methods=['GET'])
def get_watched_movies():
       try:
           token = request.headers.get('Authorization')
           logging.info(f"Authorization header: {token}")
           if not token or not token.startswith('Bearer '):
               logging.warning('Missing or invalid token')
               return jsonify({'error': 'Missing or invalid token'}), 401

           token = token.split(' ')[1]
           user_id = decode_jwt(token)
           if not user_id:
               logging.warning('Invalid or expired token')
               return jsonify({'error': 'Invalid or expired token'}), 401

           movies = get_user_watched_movies(user_id)
           logging.info(f"Returning {len(movies)} movies for user_id: {user_id}")
           return jsonify({'movies': movies}), 200
       except Exception as e:
           logging.error(f"Error in get_watched_movies: {str(e)}")
           return jsonify({'error': f"Internal server error: {str(e)}"}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid token'}), 401

        token = token.split(' ')[1]
        decoded_token = decode_token(token)
        token_jti = decoded_token['jti']  # Unikalny identyfikator tokenu
        expires = decoded_token['exp']

        # Dodaj token do blacklisty w Redis z czasem wa¿noœci
        redis_client.setex(token_jti, expires, 'blacklisted')
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500