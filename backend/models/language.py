# -*- coding: utf-8 -*-
from database import db

class MovieLanguage(db.Model):
    __tablename__ = 'movielanguage'
    language_id = db.Column("language_id", db.Integer, primary_key=True)
    language_name = db.Column("language_name", db.String(255))

class Movie_Language(db.Model):
    __tablename__ = 'movie_language'
    movie_language_id = db.Column("movie_language_id", db.Integer, primary_key=True)
    language_id = db.Column("language_id", db.Integer, db.ForeignKey('movielanguage.language_id'))
    movie_id = db.Column("movie_id", db.Integer, db.ForeignKey('movie.movie_id'))

