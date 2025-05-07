# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
import logging
from models.movie import Movie, Genre, Movie_Genre
from models.user import AppUser_Movie
from database import db

movies_bp = Blueprint('movies', __name__)

logging.basicConfig(
    filename='import.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

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

@movies_bp.route('/movies', methods=['GET'])
def get_movies():
    try:
        user_id = request.args.get('user_id', 1, type=int)
        user_movies = (
            AppUser_Movie.query
            .join(Movie, AppUser_Movie.movie_id == Movie.movie_id)
            .filter(AppUser_Movie.appuser_id == user_id, Movie.movie_type == 'movie')
            .all()
        )
        movies = [db.session.get(Movie, um.movie_id).to_dict() for um in user_movies]
        return jsonify(movies), 200
    except Exception as e:
        logging.error(f"Error fetching movies: {e}")
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