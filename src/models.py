from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    user_character_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    favorites = db.relationship('Favorites')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "user_character_id": self.user_character_id,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    character_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_year = db.Column(db.Integer)
    gender = db.Column(db.String(250))
    height = db.Column(db.Integer)
    skin_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    favorites = db.relationship('Favorites', backref='character')

    def __repr__(self):
        return '<Characters %r>' % self.character_id

    def serialize(self):
        return {
            "character_id": self.character_id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    planet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), unique=True)
    climate = db.Column(db.String(20))
    population = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    diameter = db.Column(db.Integer)
    favorites = db.relationship('Favorites', backref='planet')

    def __repr__(self):
        return '<Planets %r>' % self.planet_id

    def serialize(self):
        return {
            "planet_id": self.planet_id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter,
        }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_character_id = db.Column(db.Integer, db.ForeignKey('user.user_character_id'), nullable=False)
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.character_id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.planet_id'))
    def __repr__(self):
        return '<Favorites %r>' % self.favorite_id
    def serialize(self):
        return {
            "favorite_id": self.favorite_id,
            "characters_id": self.characters_id,
            "planets_id": self.planets_id,
            "user_character_id": self.user_character_id
        }