# -*- coding: utf-8 -*-
from database import db
from datetime import date

class AppUser(db.Model):
    __tablename__ = 'appuser'
    appuser_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.Date, default=date.today)

    def to_dict(self):
        return {
            'appuser_id': self.appuser_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AppUser_Movie(db.Model):
    __tablename__ = 'appuser_movie'
    user_movie_id = db.Column("user_movie_id", db.Integer, primary_key=True)
    appuser_id = db.Column("appuser_id", db.Integer, db.ForeignKey('appuser.appuser_id'), nullable=False)
    movie_id = db.Column("movie_id", db.Integer, db.ForeignKey('movie.movie_id'), nullable=False)
    user_rating = db.Column("user_rating", db.Float)
    watched_date = db.Column("watched_date", db.Date)

