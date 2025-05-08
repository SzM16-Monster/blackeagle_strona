from flask import Blueprint, jsonify, request
from functools import wraps
from services.auth_service import decode_jwt
from models.movie import Movie, Genre, Movie_Genre
from models.user import AppUser, AppUser_Movie
from models.language import MovieLanguage, Movie_Language
from models.people import People, Movie_People
from services.omdb_service import get_movie_from_omdb
from datetime import datetime
from database import db
import logging

omdb_bp = Blueprint('omdb', __name__)

# Configure logging
logging.basicConfig(
    filename='import.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')
        if not token:
            logging.warning('Missing token in request')
            return jsonify({'error': 'Missing token'}), 401
        user_id = decode_jwt(token)
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        user = db.session.get(AppUser, user_id)
        if not user:
            logging.warning(f'User with ID {user_id} does not exist')
            return jsonify({'error': 'User does not exist'}), 404
        request.current_user = user
        return f(*args, **kwargs)
    return decorated

@omdb_bp.route('/fetch-omdb', methods=['POST'])
@token_required
def fetch_omdb():
    try:
        data = request.get_json()
        title = data.get('title')
        user_id = request.current_user.appuser_id
        if not title:
            return jsonify({"error": "Missing movie title!"}), 400

        user = db.session.get(AppUser, user_id)
        if not user:
            return jsonify({"error": f"User with ID {user_id} does not exist!"}), 404

        movie_data = get_movie_from_omdb(title)
        if not movie_data:
            return jsonify({"error": "Movie not found in OMDB!"}), 404

        movie = Movie.query.filter_by(imdb_id=movie_data.get('imdbID')).first()
        if not movie:
            released_date = None
            if movie_data.get('Released'):
                try:
                    released_date = datetime.strptime(movie_data.get('Released'), '%d %b %Y').date()
                except ValueError:
                    logging.warning(f"Invalid date format for {movie_data.get('Title')}")

            year = movie_data.get('Year', '')
            prod_year = None
            if year and year.isdigit():
                prod_year = int(year)

            movie = Movie(
                movie_id=db.session.query(db.func.nextval('movie_movie_id_seq')).scalar(),
                title=movie_data.get('Title', '')[:255],
                prod_year=prod_year,
                rated=movie_data.get('Rated', '')[:10],
                released=released_date,
                runtime=int(movie_data.get('Runtime').split()[0]) if movie_data.get('Runtime', '').split() else None,
                plot=movie_data.get('Plot'),
                country=movie_data.get('Country', '')[:100],
                awards=movie_data.get('Awards'),
                poster=movie_data.get('Poster', '')[:255],
                tmdb_rating=None,
                rotten_tomatoes=float(movie_data.get('Ratings', [{}])[1].get('Value', '0%').strip('%')) if len(movie_data.get('Ratings', [])) > 1 else None,
                metacritic=float(movie_data.get('Metacritic', '0/100').split('/')[0]) if movie_data.get('Metacritic') else None,
                imdb_rating=float(movie_data.get('imdbRating')) if movie_data.get('imdbRating') else None,
                imdb_votes=int(movie_data.get('imdbVotes').replace(',', '')) if movie_data.get('imdbVotes', '').replace(',', '').isdigit() else None,
                imdb_id=movie_data.get('imdbID', '')[:20],
                movie_type=movie_data.get('Type', '')[:50],
                box_office=movie_data.get('BoxOffice', '')[:50]
            )
            db.session.add(movie)
            db.session.commit()

            genres = movie_data.get('Genre', '').split(', ')
            for genre in genres:
                if genre:
                    genre_obj = Genre.query.filter_by(genre_name=genre.strip()).first()
                    if not genre_obj:
                        genre_obj = Genre(
                            genre_id=db.session.query(db.func.nextval('genre_genre_id_seq')).scalar(),
                            genre_name=genre.strip()[:120]
                        )
                        db.session.add(genre_obj)
                        db.session.commit()
                    movie_genre = Movie_Genre.query.filter_by(movie_id=movie.movie_id, genre_id=genre_obj.genre_id).first()
                    if not movie_genre:
                        movie_genre = Movie_Genre(
                            movie_genre_id=db.session.query(db.func.nextval('movie_genre_movie_genre_id_seq')).scalar(),
                            movie_id=movie.movie_id,
                            genre_id=genre_obj.genre_id
                        )
                        db.session.add(movie_genre)

            languages = movie_data.get('Language', '').split(', ')
            for language in languages:
                if language:
                    language_obj = MovieLanguage.query.filter_by(language_name=language.strip()).first()
                    if not language_obj:
                        language_obj = MovieLanguage(
                            language_id=db.session.query(db.func.nextval('movielanguage_language_id_seq')).scalar(),
                            language_name=language.strip()[:255]
                        )
                        db.session.add(language_obj)
                        db.session.commit()
                    movie_language = Movie_Language.query.filter_by(movie_id=movie.movie_id, language_id=language_obj.language_id).first()
                    if not movie_language:
                        movie_language = Movie_Language(
                            movie_language_id=db.session.query(db.func.nextval('movie_language_movie_language_id_seq')).scalar(),
                            language_id=language_obj.language_id,
                            movie_id=movie.movie_id
                        )
                        db.session.add(movie_language)

            actors = movie_data.get('Actors', '').split(', ')
            for actor in actors:
                if actor:
                    person = People.query.filter_by(people_name=actor.strip()).first()
                    if not person:
                        person = People(
                            people_id=db.session.query(db.func.nextval('people_people_id_seq')).scalar(),
                            people_name=actor.strip()[:255]
                        )
                        db.session.add(person)
                        db.session.commit()
                    movie_person = Movie_People.query.filter_by(movie_id=movie.movie_id, people_id=person.people_id, role='Actor').first()
                    if not movie_person:
                        movie_person = Movie_People(
                            movie_people_id=db.session.query(db.func.nextval('movie_people_movie_people_id_seq')).scalar(),
                            movie_id=movie.movie_id,
                            people_id=person.people_id,
                            role='Actor'[:255]
                        )
                        db.session.add(movie_person)

            directors = movie_data.get('Director', '').split(', ')
            for director in directors:
                if director:
                    person = People.query.filter_by(people_name=director.strip()).first()
                    if not person:
                        person = People(
                            people_id=db.session.query(db.func.nextval('people_people_id_seq')).scalar(),
                            people_name=director.strip()[:255]
                        )
                        db.session.add(person)
                        db.session.commit()
                    movie_person = Movie_People.query.filter_by(movie_id=movie.movie_id, people_id=person.people_id, role='Director').first()
                    if not movie_person:
                        movie_person = Movie_People(
                            movie_people_id=db.session.query(db.func.nextval('movie_people_movie_people_id_seq')).scalar(),
                            movie_id=movie.movie_id,
                            people_id=person.people_id,
                            role='Director'[:255]
                        )
                        db.session.add(movie_person)

            user_movie = AppUser_Movie.query.filter_by(appuser_id=user_id, movie_id=movie.movie_id).first()
            if not user_movie:
                user_movie = AppUser_Movie(
                    user_movie_id=db.session.query(db.func.nextval('user_movie_user_movie_id_seq')).scalar(),
                    appuser_id=user_id,
                    movie_id=movie.movie_id,
                    user_rating=None,
                    watched_date=None
                )
                db.session.add(user_movie)
            db.session.commit()

        return jsonify({"message": "Movie data saved successfully!", "movie": movie.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error processing OMDB for title {title}: {str(e)}")
        return jsonify({"error": f"Error processing OMDB: {str(e)}"}), 500