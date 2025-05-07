# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
import logging
from .omdb_service import get_movie_from_omdb
from models.movie import Movie, Genre, Movie_Genre
from models.user import AppUser, AppUser_Movie
from models.language import MovieLanguage, Movie_Language
from models.people import People, Movie_People
from database import db

logging.basicConfig(
    filename='import.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def process_csv_row(row, user_id):
    title = row['Title']
    date_str = row.get('Date', None)
    try:
        watched_date = datetime.strptime(date_str, '%m/%d/%y').date() if date_str else None
        if watched_date and (watched_date.year < 1900 or watched_date.year > datetime.now().year + 1):
            logging.warning(f"Suspicious date for movie {title}: {date_str}")
            return
    except (ValueError, TypeError):
        logging.error(f"Invalid date format for movie {title}: {date_str}")
        watched_date = None

    movie_data = get_movie_from_omdb(title)
    if not movie_data:
        logging.info(f"Skipping movie {title}: not found in OMDB")
        return

    movie = Movie.query.filter_by(imdb_id=movie_data.get('imdbID')).first()
    if not movie:
        released_date = None
        if movie_data.get('Released'):
            try:
                released_date = datetime.strptime(movie_data.get('Released'), '%d %b %Y').date()
            except ValueError:
                logging.warning(f"Invalid release date format for {movie_data.get('Title')}")

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
            watched_date=watched_date
        )
        db.session.add(user_movie)
    else:
        user_movie.watched_date = watched_date or user_movie.watched_date
        db.session.add(user_movie)
    db.session.commit()