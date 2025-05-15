# -*- coding: utf-8 -*-
from lib2to3.pgen2 import token
from flask import Blueprint, jsonify, request
import logging
from services.auth_service import decode_jwt
from models.movie import Movie, Genre, Movie_Genre
from models.user import AppUser_Movie, AppUser
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.sql import func

movies_bp = Blueprint('movies', __name__)

logging.basicConfig(
    filename='import.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

@movies_bp.route('/movies', methods=['GET'])
def get_movies():
    try:
        movies = Movie.query.all()
        return jsonify([movie.to_dict() for movie in movies]), 200
    except Exception as e:
        logging.error(f"Error fetching all movies: {e}")
        return jsonify({"error": str(e)}), 500

@movies_bp.route('/movies-and-series', methods=['GET'])
def get_movies_and_series():
    try:
        user_id = request.args.get('user_id', 1, type=int)
        user_movies = AppUser_Movie.query.filter_by(appuser_id=user_id).all()
        movies = [db.session.get(Movie, um.movie_id).to_dict() for um in user_movies]
        return jsonify(movies), 200
    except Exception as e:
        logging.error(f"Error fetching movies and series: {e}")
        return jsonify({"error": str(e)}), 500

@movies_bp.route('/series', methods=['GET'])
def get_series():
    try:
        user_id = request.args.get('user_id', 1, type=int)
        user_movies = (
            AppUser_Movie.query
            .join(Movie, AppUser_Movie.movie_id == Movie.movie_id)
            .filter(AppUser_Movie.appuser_id == user_id, Movie.movie_type == 'series')
            .all()
        )
        series = [db.session.get(Movie, um.movie_id).to_dict() for um in user_movies]
        return jsonify(series), 200
    except Exception as e:
        logging.error(f"Error fetching series: {e}")
        return jsonify({"error": str(e)}), 500

@movies_bp.route('/moviesbygenre', methods=['GET'])
def get_movies_by_genre():
    try:
        user_id = request.args.get('user_id', 1, type=int)
        genre = request.args.get('genre', None)
        query = (
            AppUser_Movie.query
            .select_from(AppUser_Movie)
            .join(Movie, AppUser_Movie.movie_id == Movie.movie_id)
        )
        if genre:
            query = (
                query
                .join(Movie_Genre, Movie.movie_id == Movie_Genre.movie_id)
                .join(Genre, Movie_Genre.genre_id == Genre.genre_id)
                .filter(Genre.genre_name.ilike(genre))
            )
        movies = [db.session.get(Movie, um.movie_id).to_dict() for um in query.all()]
        return jsonify(movies), 200
    except Exception as e:
        logging.error(f"Error fetching movies by genre: {e}")
        return jsonify({"error": str(e)}), 500

@movies_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
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

        logging.info(f"Fetching recommendations for email: {user_id}")

        # Krok 1: Pobierz u¿ytkownika na podstawie email (zak³adaj¹c, ¿e user_id to email)
        user = AppUser.query.get(user_id)  
        if not user:
            logging.warning(f"User not found for email: {user_id}")
            return jsonify({"error": "User not found"}), 404

        # Krok 2: Pobierz obejrzane filmy u¿ytkownika
        watched_movies = (
            AppUser_Movie.query
            .filter(AppUser_Movie.appuser_id == user.appuser_id)
            .all()
        )
        watched_movie_ids = [movie.movie_id for movie in watched_movies]
        logging.info(f"Found {len(watched_movie_ids)} watched movies for user_id: {user.appuser_id}")

        if not watched_movies:
            logging.warning(f"No watched movies found for user_id: {user.appuser_id}")
            return jsonify({"error": "No watched movies found"}), 404

        # Krok 3: ZnajdŸ najczêœciej ogl¹dany gatunek
        genre_counts = (
            db.session.query(Genre.genre_name, func.count(Genre.genre_id).label('count'))
            .join(Movie_Genre, Genre.genre_id == Movie_Genre.genre_id)
            .join(AppUser_Movie, Movie_Genre.movie_id == AppUser_Movie.movie_id)
            .filter(AppUser_Movie.appuser_id == user.appuser_id)
            .group_by(Genre.genre_name)
            .order_by(func.count(Genre.genre_id).desc())
            .first()
        )

        if not genre_counts:
            logging.warning(f"No genres found for watched movies for user_id: {user.appuser_id}")
            return jsonify({"error": "No genres found for watched movies. Please ensure watched movies have associated genres."}), 404

        top_genre = genre_counts.genre_name
        logging.info(f"Top genre for appuser_id {user.appuser_id}: {top_genre}")

        # Krok 4: Pobierz filmy z najczêœciej ogl¹danego gatunku, które u¿ytkownik jeszcze nie ogl¹da³
        recommendations = (
            Movie.query
            .join(Movie_Genre, Movie.movie_id == Movie_Genre.movie_id)
            .join(Genre, Movie_Genre.genre_id == Genre.genre_id)
            .filter(
                Genre.genre_name == top_genre,
                Movie.movie_id.notin_(watched_movie_ids)
            )
            .order_by(Movie.imdb_rating.desc().nullslast())
            .limit(5)
            .all()
        )

        logging.info(f"Found {len(recommendations)} recommendations for genre: {top_genre}")
        return jsonify({'recommendation': [movie.to_dict() for movie in recommendations]}), 200
    except Exception as e:
        logging.error(f"Error fetching recommendations: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

