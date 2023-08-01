"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters,Planets,Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# START endpoints
@app.route('/user/<int:user_character_id>', methods=['GET'])
def find_user(user_character_id):
    user_character_id = User.query.get(user_character_id)
    if not user_character_id:
        return jsonify(message='user not found'), 404
    return jsonify(user_character_id)

@app.route('/user', methods=['GET'])
def Get_users():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200


# create one user
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    new_user = User(email=email, password=password, username=username)
    db.session.add(new_user)
    db.session.commit()

    return jsonify('new user created'), 200

@app.route('/user/favorites', methods=['GET'])
def user_faves():
    favorites = Favorites.query.all()
    all_favorites = list(map(lambda x: x.serialize(), favorites))
    return jsonify(all_favorites), 200

@app.route('/user/<int:user_character_id>', methods=['DELETE'])
def delete_user(user_character_id):
    user = User.query.get(user_character_id)
    if user is None:
        return jsonify('User not found'), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify('User deleted'), 200



#CHARACTERS
#get_all_charaters
@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Characters.query.all()
    results = list(map(lambda item: item.serialize(), characters))
    return jsonify(results), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_one_character(character_id):
    character = Characters.query.get(character_id)
    return jsonify(character.serialize()), 200

@app.route('/favorites/characters/<int:character_id>', methods=['POST'])
def fave_characters(character_id):
    favorite_characters = Favorites(user_character_id=request.get_json()['user_character_id'], characters_id=character_id)
    db.session.add(favorite_characters)
    db.session.commit()
    return jsonify('Favorite character added'), 200
#PLANETS
@app.route('/planets', methods=['GET'])
def get_planets():
    planets_query = Planets.query.all()
    results = list(map(lambda item: item.serialize(), planets_query))
    return jsonify(results), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planets(planet_id):
    planet_query = Planets.query.get(planet_id)
    return jsonify(planet_query.serialize()), 200

@app.route('/favorites/planets/<int:planet_id>', methods=['POST'])
def fave_planets(planet_id):
    favorite_planets = Favorites(user_character_id=request.get_json()['user_character_id'], planets_id=planet_id)
    db.session.add(favorite_planets)
    db.session.commit()
    return jsonify('Favorite planet added'), 200

#Favorites
@app.route('/favorites/planets/<int:planets_id>', methods=['DELETE'])
def delete_favorite_planet(planets_id):
    favorite_planets = Favorites.query.filter_by(user_character_id = request.get_json()['user_character_id'], planet_id=planets_id).first()
    if favorite_planets is None:
        return jsonify('Planet not found')
    db.session.delete(favorite_planets)
    return jsonify('favorite planet deleted')


@app.route('/favorites/characters/<int:character_id>', methods=['DELETE'])
def delete_favorite_characters(character_id):
    favorite_characters = Favorites.query.filter_by(user_character_id = request.get_json()['user_character_id'], character_id=character_id).first()
    if favorite_characters is None:
        return jsonify('characters not found')
    db.session.delete(favorite_characters)
    return jsonify('favorite characters deleted')
# END endpoints

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)