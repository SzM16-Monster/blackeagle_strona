from app import app, db, User, Movie, User_Movie
from sqlalchemy import text
from datetime import date

with app.app_context():
    # Usuwanie istniejacych danych
    db.session.execute(text('DELETE FROM User_Movie;'))
    db.session.execute(text('DELETE FROM Movie;'))
    db.session.execute(text('DELETE FROM "User";'))
    db.session.commit()

    # Dodanie uzytkownika
    user = User(
        user_id=1,
        first_name="Test",
        last_name="User",
        email="test@example.com",
        username="test_user",
        password="hashed_password",
        created_at=date(2023, 10, 1)
    )
    db.session.add(user)
    
    # Dodanie filmu
    movie = Movie(
        movie_id=1,
        title="Inception",
        year=2010,
        rated="PG-13",
        released=date(2010, 7, 16),
        runtime=148,
        plot="A thief enters dreams to steal secrets.",
        country="USA",
        awards="Won 4 Oscars",
        poster="https://via.placeholder.com/200x300",
        movie_database=8.8,
        rotten_tomatoes=87.0,
        metacritic=74.0,
        metascore=74.0,
        imdb_rating=8.8,
        imdb_votes=2500000,
        imdb_id="tt1375666",
        type="movie",
        box_office="$829,895,144",
        response="True"
    )
    db.session.add(movie)
    db.session.commit()
    
    # Dodanie powiazania uzytkownik-film
    user_movie = User_Movie(
        user_movie_id=1,
        user_id=user.user_id,
        movie_id=movie.movie_id,
        user_rated="8.5"
    )
    db.session.add(user_movie)
    db.session.commit()

    print("Test data added successfully!")