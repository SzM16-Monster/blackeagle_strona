# -*- coding: utf-8 -*-
from database import db

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

class Genre(db.Model):
    __tablename__ = 'genre'
    genre_id = db.Column("genre_id", db.Integer, primary_key=True)
    genre_name = db.Column("genre_name", db.String(120))

class Movie_Genre(db.Model):
    __tablename__ = 'movie_genre'
    movie_genre_id = db.Column("movie_genre_id", db.Integer, primary_key=True)
    movie_id = db.Column("movie_id", db.Integer, db.ForeignKey('movie.movie_id'))
    genre_id = db.Column("genre_id", db.Integer, db.ForeignKey('genre.genre_id'))