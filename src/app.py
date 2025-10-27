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
from models import db, User, Characters, FavoriteCharacters, Planets, FavoritePlanets, Starships, FavoriteStarships
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




@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())
    response_body = {
        'users': users_serialized
    }
    return jsonify(response_body), 200


@app.route('/users', methods=['POST'])
def add_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'debes introducir información'}), 400
    
    if 'email' not in body:
        return jsonify({'msg': 'debes introducir un email'}), 400
    if 'password' not in body:
        return jsonify({'msg': ' debes introducir una contraseña'}), 400

    
    new_user = User()
    new_user.email = body['email']
    new_user.password = body['password']
    new_user.is_active = True
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'Ususario registrado', 'user': new_user.serialize()}), 200


@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    characters_list = []
    for character in characters:
        characters_list.append(character.serialize())
    response_body = {
        'characters': characters_list
    }
    return jsonify(response_body), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Characters.query.get(character_id)
    if character:
        response_body = {'character': character.serialize()}
        return jsonify(response_body), 200
    return jsonify({'msg': 'Character not found'}), 400


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets_list = []
    for planet in planets:
        planets_list.append(planet.serialize())
    response_body = {
        'planets': planets_list
    }
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet:
        response_body = {'planet': planet.serialize()}
        return jsonify(response_body), 200
    return jsonify({'msg': 'Planet not found'}), 400


@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starships.query.all()
    starships_list = []
    for starship in starships:
        starships_list.append(starship.serialize())
    response_body = {
        'starships': starships_list
    }
    return jsonify(response_body), 200

@app.route('/starships/<int:starship_id>', methods=['GET'])
def get_starship(starship_id):
    starship = Starships.query.get(starship_id)
    if starship:
        response_body = {'starship': starship.serialize()}
        return jsonify(response_body), 200
    return jsonify({'msg': 'Starship not found'}), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
