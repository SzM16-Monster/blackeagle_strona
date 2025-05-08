# -*- coding: utf-8 -*-
from database import db

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
