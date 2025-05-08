from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from database import db
from api.movies import movies_bp
from api.omdb import omdb_bp
from api.csv import csv_bp
from api.auth import auth_bp

def create_app():
       app = Flask(__name__)
       app.config.from_object(Config)
       # Enable CORS for specified origins
       CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGINS}})

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

       return app
app = create_app()
if __name__ == '__main__':
      
       app.run(debug=True)