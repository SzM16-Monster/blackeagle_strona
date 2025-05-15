from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from database import db
from api.movies import movies_bp
from api.omdb import omdb_bp
from api.csv import csv_bp
from api.auth import auth_bp
import logging
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configure logging
    logging.basicConfig(
        filename='app.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8'
    )

    # Enable CORS
    CORS(app, resources={r"/*": {
        "origins": Config.CORS_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Authorization", "Content-Type"]
    }})

    jwt = JWTManager(app)
    # Initialize database
    db.init_app(app)
    # Initialize migrations
    migrate = Migrate(app, db)

    # Register blueprints
    app.register_blueprint(movies_bp)
    app.register_blueprint(omdb_bp)
    app.register_blueprint(csv_bp)
    app.register_blueprint(auth_bp)

    # Add UTF-8 header to all JSON responses
    @app.after_request
    def add_utf8_header(response):
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    # Log all requests
    #@app.before_request
    #def log_request():
    #    logging.info(f"Request: {request.method} {request.path} Headers: {request.headers}")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)