import pandas as pd
import psycopg2
import requests
from urllib.parse import quote, urlparse
from datetime import datetime
import logging
import argparse

# Configuration
DATABASE_URL_LOCAL = 'postgresql://postgres@localhost:5432/black_eagle'  # Local database
DATABASE_URL_RENDER = 'postgresql://feste790_user:8OrKT0R6yqZrETJ1fy4hMB486B9h9Txk@dpg-d06h50ili9vc73ecgr10-a.oregon-postgres.render.com/black_eagle_db'  # Render
OMDB_API_KEY = '5da8ff81'
CSV_FILE = 'another.csv'
LOG_FILE = 'import.log'

# Logging configuration
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to parse DATABASE_URL
def parse_db_url(db_url):
    parsed_url = urlparse(db_url)
    return {
        'dbname': parsed_url.path[1:],
        'user': parsed_url.username,
        'password': parsed_url.password,
        'host': parsed_url.hostname,
        'port': parsed_url.port
    }

# Function to connect to the database
def get_db_connection(db_url):
    try:
        conn = psycopg2.connect(**parse_db_url(db_url))
        return conn
    except psycopg2.Error as e:
        logging.error(f"Database connection error: {e}")
        raise

# Function to get appuser_id based on email
def get_user_id(conn, email):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT appuser_id FROM appuser WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result:
            return result[0]
        logging.error(f"User with email not found: {email}")
        return None
    except psycopg2.Error as e:
        logging.error(f"Error fetching appuser_id for {email}: {e}")
        return None
    finally:
        cursor.close()

# Function to fetch data from OMDB
def get_movie_from_omdb(title):
    url = f'http://www.omdbapi.com/?t={quote(title)}&apikey={OMDB_API_KEY}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                # Poster validation
                poster = data.get('Poster', '')
                if poster and not poster.startswith('http'):
                    logging.warning(f"Invalid poster URL for {title}: {poster}")
                    data['Poster'] = None
                return data
            else:
                logging.warning(f"Movie not found in OMDB: {title}")
                return None
        else:
            logging.error(f"API error for {title}: {response.status_code}")
            return None
    except requests.RequestException as e:
        logging.error(f"Request error to OMDB for {title}: {e}")
        return None

# Function to insert or get movie_id
def insert_or_get_movie(conn, movie_data):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT movie_id FROM movie WHERE imdb_id = %s", (movie_data.get('imdbID'),))
        result = cursor.fetchone()
        if result:
            return result[0]

        released_date = None
        if movie_data.get('Released'):
            try:
                released_date = datetime.strptime(movie_data.get('Released'), '%d %b %Y').date()
            except ValueError:
                logging.warning(f"Invalid release date format for {movie_data.get('Title')}: {movie_data.get('Released')}")

        cursor.execute("""
            INSERT INTO movie (
                movie_id, title, prod_year, rated, released, runtime, plot, country, awards, poster,
                tmdb_rating, rotten_tomatoes, metacritic, imdb_rating, imdb_votes, imdb_id, movie_type, box_office
            ) VALUES (nextval('movie_movie_id_seq'), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING movie_id
        """, (
            movie_data.get('Title', '')[:255],
            int(movie_data.get('Year')) if movie_data.get('Year', '').isdigit() else None,
            movie_data.get('Rated', '')[:10],
            released_date,
            int(movie_data.get('Runtime').split()[0]) if movie_data.get('Runtime', '').split() else None,
            movie_data.get('Plot'),
            movie_data.get('Country', '')[:100],
            movie_data.get('Awards'),
            movie_data.get('Poster', '')[:255],
            None,
            float(movie_data.get('Ratings', [{}])[1].get('Value', '0%').strip('%')) if len(movie_data.get('Ratings', [])) > 1 else None,
            float(movie_data.get('Metacritic', '0/100').split('/')[0]) if movie_data.get('Metacritic') else None,
            float(movie_data.get('imdbRating')) if movie_data.get('imdbRating') else None,
            int(movie_data.get('imdbVotes').replace(',', '')) if movie_data.get('imdbVotes', '').replace(',', '').isdigit() else None,
            movie_data.get('imdbID', '')[:20],
            movie_data.get('Type', '')[:50],
            movie_data.get('BoxOffice', '')[:50]
        ))
        movie_id = cursor.fetchone()[0]
        conn.commit()
        logging.info(f"Added movie: {movie_data.get('Title')} (movie_id: {movie_id})")
        return movie_id
    except psycopg2.Error as e:
        logging.error(f"Error inserting movie {movie_data.get('Title')}: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

# Function to insert or get genre_id
def insert_or_get_genre(conn, genre_name):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT genre_id FROM genre WHERE genre_name = %s", (genre_name,))
        result = cursor.fetchone()
        if result:
            return result[0]

        cursor.execute("INSERT INTO genre (genre_id, genre_name) VALUES (nextval('genre_genre_id_seq'), %s) RETURNING genre_id", (genre_name[:120],))
        genre_id = cursor.fetchone()[0]
        conn.commit()
        logging.info(f"Added genre: {genre_name} (genre_id: {genre_id})")
        return genre_id
    except psycopg2.Error as e:
        logging.error(f"Error inserting genre {genre_name}: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

# Function to insert movie-genre relationship
def insert_movie_genre(conn, movie_id, genre_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT movie_genre_id FROM movie_genre WHERE movie_id = %s AND genre_id = %s", (movie_id, genre_id))
        if cursor.fetchone():
            return
        cursor.execute("INSERT INTO movie_genre (movie_genre_id, movie_id, genre_id) VALUES (nextval('movie_genre_movie_genre_id_seq'), %s, %s)", (movie_id, genre_id))
        conn.commit()
    except psycopg2.Error as e:
        logging.error(f"Error inserting movie_genre relationship (movie_id: {movie_id}, genre_id: {genre_id}): {e}")
        conn.rollback()
    finally:
        cursor.close()

# Function to insert or get language_id
def insert_or_get_language(conn, language_name):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT language_id FROM movielanguage WHERE language_name = %s", (language_name,))
        result = cursor.fetchone()
        if result:
            return result[0]

        cursor.execute("INSERT INTO movielanguage (language_id, language_name) VALUES (nextval('movielanguage_language_id_seq'), %s) RETURNING language_id", (language_name[:255],))
        language_id = cursor.fetchone()[0]
        conn.commit()
        logging.info(f"Added language: {language_name} (language_id: {language_id})")
        return language_id
    except psycopg2.Error as e:
        logging.error(f"Error inserting language {language_name}: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

# Function to insert movie-language relationship
def insert_movie_language(conn, movie_id, language_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT movie_language_id FROM movie_language WHERE movie_id = %s AND language_id = %s", (movie_id, language_id))
        if cursor.fetchone():
            return
        cursor.execute("INSERT INTO movie_language (movie_language_id, language_id, movie_id) VALUES (nextval('movie_language_movie_language_id_seq'), %s, %s)", (language_id, movie_id))
        conn.commit()
    except psycopg2.Error as e:
        logging.error(f"Error inserting movie_language relationship (movie_id: {movie_id}, language_id: {language_id}): {e}")
        conn.rollback()
    finally:
        cursor.close()

# Function to insert or get person_id
def insert_or_get_person(conn, person_name):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT people_id FROM people WHERE people_name = %s", (person_name,))
        result = cursor.fetchone()
        if result:
            return result[0]

        cursor.execute("INSERT INTO people (people_id, people_name) VALUES (nextval('people_people_id_seq'), %s) RETURNING people_id", (person_name[:255],))
        person_id = cursor.fetchone()[0]
        conn.commit()
        logging.info(f"Added person: {person_name} (people_id: {person_id})")
        return person_id
    except psycopg2.Error as e:
        logging.error(f"Error inserting person {person_name}: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

# Function to insert movie-person relationship
def insert_movie_person(conn, movie_id, person_id, role):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT movie_people_id FROM movie_people WHERE movie_id = %s AND people_id = %s AND role = %s", (movie_id, person_id, role))
        if cursor.fetchone():
            return
        cursor.execute("INSERT INTO movie_people (movie_people_id, movie_id, people_id, role) VALUES (nextval('movie_people_movie_people_id_seq'), %s, %s, %s)", (movie_id, person_id, role[:255]))
        conn.commit()
    except psycopg2.Error as e:
        logging.error(f"Error inserting movie_people relationship (movie_id: {movie_id}, people_id: {person_id}, role: {role}): {e}")
        conn.rollback()
    finally:
        cursor.close()

# Function to insert user-movie watch information
def insert_user_movie(conn, appuser_id, movie_id, watched_date):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_movie_id FROM appuser_movie WHERE appuser_id = %s AND movie_id = %s", (appuser_id, movie_id))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO appuser_movie (user_movie_id, appuser_id, movie_id, user_rating, watched_date)
                VALUES (nextval('user_movie_user_movie_id_seq'), %s, %s, %s, %s)
            """, (appuser_id, movie_id, None, watched_date))
            conn.commit()
            logging.info(f"Added appuser_movie relationship (appuser_id: {appuser_id}, movie_id: {movie_id})")
        else:
            logging.info(f"Relationship appuser_movie already exists (appuser_id: {appuser_id}, movie_id: {movie_id})")
    except psycopg2.Error as e:
        logging.error(f"Error inserting appuser_movie relationship (appuser_id: {appuser_id}, movie_id: {movie_id}): {e}")
        conn.rollback()
    finally:
        cursor.close()

# Main processing function
def process_movies(email, csv_file, use_local_db):
    db_url = DATABASE_URL_LOCAL if use_local_db else DATABASE_URL_RENDER
    try:
        df = pd.read_csv(csv_file)
        print(f"Found {len(df)} movies in {csv_file}")
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file}")
        logging.error(f"CSV file not found: {csv_file}")
        return
    except pd.errors.EmptyDataError:
        print(f"CSV file is empty: {csv_file}")
        logging.error(f"CSV file is empty: {csv_file}")
        return

    conn = get_db_connection(db_url)
    appuser_id = get_user_id(conn, email)
    if not appuser_id:
        print(f"User with email not found: {email}")
        conn.close()
        return

    for index, row in df.iterrows():
        title = row['Title']
        date_str = row.get('Date', None)
        logging.info(f"Processing movie: {title}")
        print(f"Processing movie: {title}")

        try:
            watched_date = datetime.strptime(date_str, '%m/%d/%y').date() if date_str else datetime.now().date()
            if watched_date.year < 1900 or watched_date.year > datetime.now().year + 1:
                logging.warning(f"Suspicious date for movie {title}: {date_str}")
                continue
        except (ValueError, TypeError):
            logging.error(f"Invalid date format for movie {title}: {date_str}")
            watched_date = datetime.now().date()

        movie_data = get_movie_from_omdb(title)
        if not movie_data:
            continue

        movie_id = insert_or_get_movie(conn, movie_data)
        if not movie_id:
            continue

        genres = movie_data.get('Genre', '').split(', ')
        for genre in genres:
            if genre:
                genre_id = insert_or_get_genre(conn, genre.strip())
                if genre_id:
                    insert_movie_genre(conn, movie_id, genre_id)

        languages = movie_data.get('Language', '').split(', ')
        for language in languages:
            if language:
                language_id = insert_or_get_language(conn, language.strip())
                if language_id:
                    insert_movie_language(conn, movie_id, language_id)

        actors = movie_data.get('Actors', '').split(', ')
        for actor in actors:
            if actor:
                actor_id = insert_or_get_person(conn, actor.strip())
                if actor_id:
                    insert_movie_person(conn, movie_id, actor_id, 'Actor')

        directors = movie_data.get('Director', '').split(', ')
        for director in directors:
            if director:
                director_id = insert_or_get_person(conn, director.strip())
                if director_id:
                    insert_movie_person(conn, movie_id, director_id, 'Director')

        insert_user_movie(conn, appuser_id, movie_id, watched_date)

    conn.close()
    logging.info("Processing completed.")
    print("Processing completed. Check logs in import.log.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import movies to Black-Eagle database")
    parser.add_argument('--email', type=str, required=True, help="Email of the user (e.g., szymek2@gmail.com)")
    parser.add_argument('--csv', type=str, default=CSV_FILE, help="Path to CSV file with movie titles")
    parser.add_argument('--local', action='store_true', help="Use local database instead of Render")
    args = parser.parse_args()

    process_movies(args.email, args.csv, args.local)