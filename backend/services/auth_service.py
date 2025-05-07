import bcrypt
import jwt
import datetime
from config import Config
from database import db
from models.user import AppUser
import logging

# Configure logging
logging.basicConfig(
    filename='import.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def hash_password(password):
    return bcrypt.hashpw(password.encode('ascii'), bcrypt.gensalt()).decode('ascii')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('ascii'), hashed_password.encode('ascii'))

def generate_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def decode_jwt(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        logging.error('Token expired')
        return None
    except jwt.InvalidTokenError:
        logging.error('Invalid token')
        return None

def register_user(first_name, last_name, email, username, password):
    if AppUser.query.filter_by(username=username).first() or AppUser.query.filter_by(email=email).first():
        logging.warning(f'Registration failed: username {username} or email {email} already exists')
        return None
    hashed_password = hash_password(password)
    user = AppUser(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
        password=hashed_password,
        created_at=datetime.date.today()
    )
    db.session.add(user)
    db.session.commit()
    logging.info(f'User created: {username}')
    return user

def login_user(email, password):
    user = AppUser.query.filter_by(email=email).first()
    if user and verify_password(password, user.password):
        token = generate_jwt(user.appuser_id)
        logging.info(f'User logged in: {email}')
        return token
    logging.warning(f'Login failed for: {email}')
    return None