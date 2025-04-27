from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import requests
from urllib.parse import quote
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

# Konfiguracja logowania
logging.basicConfig(filename='import.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ładowanie zmiennych środowiskowych
load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY', '5da8ff81')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:3000",
    "https://moj-frontend.vercel.app",
    "https://frontend-6led4jy72-feste790s-projects.vercel.app",
    "frontend-git-main-feste790s-projects.vercel.app"
]}})
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:haslo123@localhost:5432/black_eagle_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modele zgodne z Twoim schematem
class AppUser(db.Model):
    __tablename__ = 'appuser'
    appuser_id = db.Column("appuser_id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(255))
    last_name = db.Column("last_name", db.String(255))
    email = db.Column("email", db.String(255), nullable=False, unique=True)
    username = db.Column("username", db.String(255), nullable=False, unique=True)
    password = db.Column("password", db.String(255), nullable=False)
    created_at = db.Column("created_at", db.Date)

class Movie(db.Model):
    __tablename__ = 'movie'
    movie_id = db.Column("movie_id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(255), nullable=False)
    prod_year = db.Column("prod_year", db.Integer)
    rated = db.Column("rated", db.String(10))
    released = db.Column("released", db.Date)
    runtime = db.Column("runtime", db.Integer)
    plot = db.Column("plot", db.Text)
    country = db.Column("country", db.String(100))
    awards = db.Column("awards", db.Text)
    poster = db.Column("poster", db.String(255))
    tmdb_rating = db.Column("tmdb_rating", db.Float)
    rotten_tomatoes = db.Column("rotten_tomatoes", db.Float)
    metacritic = db.Column("metacritic", db.Float)
    imdb_rating = db.Column("imdb_rating", db.Float)
    imdb_votes = db.Column("imdb_votes", db.Integer)
    imdb_id = db.Column("imdb_id", db.String(20))
    movie_type = db.Column("movie_type", db.String(50))
    box_office = db.Column("box_office", db.String(50))

    def to_dict(self):
        return {
            'movie_id': self.movie_id,
            'title': self.title,
            'prod_year': self.prod_year,
            'rated': self.rated,
            'released': self.released.isoformat() if self.released else None,
            'runtime': self.runtime,
            'plot': self.plot,
            'country': self.country,
            'awards': self.awards,
            'poster': self.poster,
            'tmdb_rating': self.tmdb_rating,
            'rotten_tomatoes': self.rotten_tomatoes,
            'metacritic': self.metacritic,
            'imdb_rating': self.imdb_rating,
            'imdb_votes': self.imdb_votes,
            'imdb_id': self.imdb_id,
            'movie_type': self.movie_type,
            'box_office': self.box_office
        }

class AppUser_Movie(db.Model):
    __tablename__ = 'appuser_movie'
    user_movie_id = db.Column("user_movie_id", db.Integer, primary_key=True)
    appuser_id = db.Column("appuser_id", db.Integer, db.ForeignKey('appuser.appuser_id'), nullable=False)
    movie_id = db.Column("movie_id", db.Integer, db.ForeignKey('movie.movie_id'), nullable=False)
    user_rating = db.Column("user_rating", db.Float)
    watched_date = db.Column("watched_date", db.Date)

class Genre(db.Model):
    __tablename__ = 'genre'
    genre_id = db.Column("genre_id", db.Integer, primary_key=True)
    genre_name = db.Column("genre_name", db.String(120))

class Movie_Genre(db.Model):
    __tablename__ = 'movie_genre'
    movie_genre_id = db.Column("movie_genre_id", db.Integer, primary_key=True)
    movie_id = db.Column("movie_id", db.Integer, db.ForeignKey('movie.movie_id'))
    genre_id = db.Column("genre_id", db.Integer, db.ForeignKey('genre.genre_id'))

class MovieLanguage(db.Model):
    __tablename__ = 'movielanguage'
    language_id = db.Column("language_id", db.Integer, primary_key=True)
    language_name = db.Column("language_name", db.String(255))

class Movie_Language(db.Model):
    __tablename__ = 'movie_language'
    movie_language_id = db.Column("movie_language_id", db.Integer, primary_key=True)
    language_id = db.Column("language_id", db.Integer, db.ForeignKey('movielanguage.language_id'))
    movie_id = db.Column("movie_id", db.Integer, db.ForeignKey('movie.movie_id'))

class People(db.Model):
    __tablename__ = 'people'
    people_id = db.Column("people_id", db.Integer, primary_key=True)
    people_name = db.Column("people_name", db.String(255))

class Movie_People(db.Model):
    __tablename__ = 'movie_people'
    movie_people_id = db.Column("movie_people_id", db.Integer, primary_key=True)
    movie_id = db.Column("movie_id", db.Integer, db.ForeignKey('movie.movie_id'))
    people_id = db.Column("people_id", db.Integer, db.ForeignKey('people.people_id'))
    role = db.Column("role", db.String(255))

# Funkcja do pobierania danych z OMDB
def get_movie_from_omdb(title):
    url = f'http://www.omdbapi.com/?t={quote(title)}&apikey={OMDB_API_KEY}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                return data
            else:
                logging.warning(f"Nie znaleziono filmu w OMDB: {title}")
                return None
        else:
            logging.error(f"Błąd API dla {title}: {response.status_code}")
            return None
    except requests.RequestException as e:
        logging.error(f"Błąd zapytania do OMDB dla {title}: {e}")
        return None

# Endpoint do zwracania listy filmów użytkownika
@app.route('/movies', methods=['GET'])
def get_movies():
    try:
        user_id = request.args.get('user_id', 1, type=int)
        user_movies = AppUser_Movie.query.filter_by(appuser_id=user_id).all()
        movies = [db.session.get(Movie, um.movie_id).to_dict() for um in user_movies]
        return jsonify(movies), 200
    except Exception as e:
        logging.error(f"Błąd pobierania filmów: {e}")
        return jsonify({"error": str(e)}), 500

# Endpoint do wgrywania CSV
@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Brak pliku CSV!"}), 400
        file = request.files['file']
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "Plik musi być CSV!"}), 400

        user_id = request.form.get('user_id', 1, type=int)
        user = db.session.get(AppUser, user_id)
        if not user:
            return jsonify({"error": f"Użytkownik o ID {user_id} nie istnieje!"}), 404

        df = pd.read_csv(file)
        for _, row in df.iterrows():
            title = row['Title']
            date_str = row.get('Date', None)
            try:
                watched_date = datetime.strptime(date_str, '%m/%d/%y').date() if date_str else None
                if watched_date and (watched_date.year < 1900 or watched_date.year > datetime.now().year + 1):
                    logging.warning(f"Podejrzana data dla filmu {title}: {date_str}")
                    continue
            except (ValueError, TypeError):
                logging.error(f"Nieprawidłowy format daty dla filmu {title}: {date_str}")
                watched_date = None

            movie_data = get_movie_from_omdb(title)
            if not movie_data:
                logging.info(f"Pomijanie filmu {title}: brak danych w OMDB")
                continue

            # Wstaw film
            movie = Movie.query.filter_by(imdb_id=movie_data.get('imdbID')).first()
            if not movie:
                released_date = None
                if movie_data.get('Released'):
                    try:
                        released_date = datetime.strptime(movie_data.get('Released'), '%d %b %Y').date()
                    except ValueError:
                        logging.warning(f"Nieprawidłowy format daty premiery dla {movie_data.get('Title')}")
                
                # Poprawka dla Year: obsługa 'N/A' i innych niepoprawnych wartości
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

            # Wstaw gatunki
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
                    # Sprawdzanie, czy powiązanie już istnieje
                    movie_genre = Movie_Genre.query.filter_by(movie_id=movie.movie_id, genre_id=genre_obj.genre_id).first()
                    if not movie_genre:
                        movie_genre = Movie_Genre(
                            movie_genre_id=db.session.query(db.func.nextval('movie_genre_movie_genre_id_seq')).scalar(),
                            movie_id=movie.movie_id,
                            genre_id=genre_obj.genre_id
                        )
                        db.session.add(movie_genre)

            # Wstaw języki
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
                    # Sprawdzanie, czy powiązanie już istnieje
                    movie_language = Movie_Language.query.filter_by(movie_id=movie.movie_id, language_id=language_obj.language_id).first()
                    if not movie_language:
                        movie_language = Movie_Language(
                            movie_language_id=db.session.query(db.func.nextval('movie_language_movie_language_id_seq')).scalar(),
                            language_id=language_obj.language_id,
                            movie_id=movie.movie_id
                        )
                        db.session.add(movie_language)

            # Wstaw aktorów
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
                    # Sprawdzanie, czy powiązanie już istnieje
                    movie_person = Movie_People.query.filter_by(movie_id=movie.movie_id, people_id=person.people_id, role='Actor').first()
                    if not movie_person:
                        movie_person = Movie_People(
                            movie_people_id=db.session.query(db.func.nextval('movie_people_movie_people_id_seq')).scalar(),
                            movie_id=movie.movie_id,
                            people_id=person.people_id,
                            role='Actor'[:255]
                        )
                        db.session.add(movie_person)

            # Wstaw reżyserów
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
                    # Sprawdzanie, czy powiązanie już istnieje
                    movie_person = Movie_People.query.filter_by(movie_id=movie.movie_id, people_id=person.people_id, role='Director').first()
                    if not movie_person:
                        movie_person = Movie_People(
                            movie_people_id=db.session.query(db.func.nextval('movie_people_movie_people_id_seq')).scalar(),
                            movie_id=movie.movie_id,
                            people_id=person.people_id,
                            role='Director'[:255]
                        )
                        db.session.add(movie_person)

            # Wstaw powiązanie użytkownika z filmem (tylko jeśli nie istnieje)
            user_movie = AppUser_Movie.query.filter_by(appuser_id=user_id, movie_id=movie.movie_id).first()
            if not user_movie:
                user_movie = AppUser_Movie(
                    user_movie_id=db.session.query(db.func.nextval('user_movie_user_movie_id_seq')).scalar(),
                    appuser_id=user_id,
                    movie_id=movie.movie_id,
                    user_rating=None,
                    watched_date=watched_date
                )
                db.session.add(user_movie)
            else:
                # Aktualizuj watched_date, jeśli istnieje
                user_movie.watched_date = watched_date or user_movie.watched_date
                db.session.add(user_movie)
            db.session.commit()

        return jsonify({"message": "CSV przetworzone pomyślnie!"}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Błąd przetwarzania CSV dla tytułu {title}: {str(e)}")
        return jsonify({"error": f"Błąd przetwarzania CSV: {str(e)}"}), 500

# Endpoint do pobierania danych z OMDB
@app.route('/fetch-omdb', methods=['POST'])
def fetch_omdb():
    try:
        data = request.get_json()
        title = data.get('title')
        user_id = data.get('user_id', 1, type=int)
        if not title:
            return jsonify({"error": "Brak tytułu filmu!"}), 400

        user = db.session.get(AppUser, user_id)
        if not user:
            return jsonify({"error": f"Użytkownik o ID {user_id} nie istnieje!"}), 404

        movie_data = get_movie_from_omdb(title)
        if not movie_data:
            return jsonify({"error": "Film nie znaleziony w OMDB!"}), 404

        movie = Movie.query.filter_by(imdb_id=movie_data.get('imdbID')).first()
        if not movie:
            released_date = None
            if movie_data.get('Released'):
                try:
                    released_date = datetime.strptime(movie_data.get('Released'), '%d %b %Y').date()
                except ValueError:
                    logging.warning(f"Nieprawidłowy format daty premiery dla {movie_data.get('Title')}")
            
            # Poprawka dla Year: obsługa 'N/A' i innych niepoprawnych wartości
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

            # Wstaw gatunki
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
                    # Sprawdzanie, czy powiązanie już istnieje
                    movie_genre = Movie_Genre.query.filter_by(movie_id=movie.movie_id, genre_id=genre_obj.genre_id).first()
                    if not movie_genre:
                        movie_genre = Movie_Genre(
                            movie_genre_id=db.session.query(db.func.nextval('movie_genre_movie_genre_id_seq')).scalar(),
                            movie_id=movie.movie_id,
                            genre_id=genre_obj.genre_id
                        )
                        db.session.add(movie_genre)

            # Wstaw języki
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
                    # Sprawdzanie, czy powiązanie już istnieje
                    movie_language = Movie_Language.query.filter_by(movie_id=movie.movie_id, language_id=language_obj.language_id).first()
                    if not movie_language:
                        movie_language = Movie_Language(
                            movie_language_id=db.session.query(db.func.nextval('movie_language_movie_language_id_seq')).scalar(),
                            language_id=language_obj.language_id,
                            movie_id=movie.movie_id
                        )
                        db.session.add(movie_language)

            # Wstaw aktorów
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
                    # Sprawdzanie, czy powiązanie już istnieje
                    movie_person = Movie_People.query.filter_by(movie_id=movie.movie_id, people_id=person.people_id, role='Actor').first()
                    if not movie_person:
                        movie_person = Movie_People(
                            movie_people_id=db.session.query(db.func.nextval('movie_people_movie_people_id_seq')).scalar(),
                            movie_id=movie.movie_id,
                            people_id=person.people_id,
                            role='Actor'[:255]
                        )
                        db.session.add(movie_person)

            # Wstaw reżyserów
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
                    # Sprawdzanie, czy powiązanie już istnieje
                    movie_person = Movie_People.query.filter_by(movie_id=movie.movie_id, people_id=person.people_id, role='Director').first()
                    if not movie_person:
                        movie_person = Movie_People(
                            movie_people_id=db.session.query(db.func.nextval('movie_people_movie_people_id_seq')).scalar(),
                            movie_id=movie.movie_id,
                            people_id=person.people_id,
                            role='Director'[:255]
                        )
                        db.session.add(movie_person)

            # Wstaw powiązanie użytkownika z filmem (tylko jeśli nie istnieje)
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

        return jsonify({"message": "Dane filmu zapisane!", "movie": movie.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Błąd przetwarzania OMDB dla tytułu {title}: {str(e)}")
        return jsonify({"error": f"Błąd przetwarzania OMDB: {str(e)}"}), 500

@app.route('/moviesbygenre', methods=['GET'])
def get_movies_by_genre():
    try:
        user_id = request.args.get('user_id', 1, type=int)
        genre = request.args.get('genre', None)
        query = AppUser_Movie.query.filter_by(appuser_id=user_id)
        if genre:
            query = query.join(Movie_Genre).join(Genre).filter(Genre.genre_name == genre)
        movies = [db.session.get(Movie, um.movie_id).to_dict() for um in query.all()]
        return jsonify(movies), 200
    except Exception as e:
        logging.error(f"Błąd pobierania filmów: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
