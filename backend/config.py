from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OMDB_API_KEY = environ.get('OMDB_API_KEY', '5da8ff81')
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY', 'your-secret-key-very-long-and-random')
    CORS_ORIGINS = environ.get('CORS_ORIGINS', 'http://localhost:3000,https://moj-frontend.vercel.app,https://frontend-6led4jy72-feste790s-projects.vercel.app,https://frontend-git-main-feste790s-projects.vercel.app,https://frontend-feste790s-projects.vercel.app').split(',')