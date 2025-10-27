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


       
                                                #ENDPOINTS

                #Users/favorites

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
    return jsonify({'msg': 'Usuario registrado', 'user': new_user.serialize()}), 200

@app.route('/user_favorites/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404
    
    favorite_characters_serialized = []
    favorite_planets_serialized = []
    favorite_starships_serialized = []

    for registro in user.favorite_characters:
        if registro.character:
            favorite_characters_serialized.append(registro.character.serialize())
    for registro in user.favorite_planets:
        if registro.planet:
            favorite_planets_serialized.append(registro.planet.serialize())
    for registro in user.favorite_starships:
        if registro.starship:
            favorite_starships_serialized.append(registro.starship.serialize())

    return jsonify({'favorite_characters': favorite_characters_serialized,'favorite_planets': favorite_planets_serialized,'favorite_starships': favorite_starships_serialized}), 200
        

        
                #Characters

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
    return jsonify({'msg': 'Character not found'}), 404


@app.route('/favorite/<int:user_id>/character/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404
    character = Characters.query.get(character_id)
    if not character:
        return jsonify({'msg': f'El personaje con id {character_id} no existe'}), 404

    if any(fav.characters_id == character_id for fav in user.favorite_characters):
        return jsonify({'msg': 'El personaje ya está en favoritos'}), 400

    favorite = FavoriteCharacters(user_id=user.id, characters_id=character.id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'msg': 'Personaje agregado a favoritos'}), 200


@app.route('/favorite/<int:user_id>/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404

    favorite = FavoriteCharacters.query.filter_by(user_id=user.id, characters_id=character_id).first()
    if not favorite:
        return jsonify({'msg': f'El personaje con id {character_id} no está en favoritos'}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'msg': 'Personaje eliminado de favoritos'}), 200




                #Planets

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
    return jsonify({'msg': 'Planet not found'}), 404


@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404

    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({'msg': f'El planeta con id {planet_id} no existe'}), 404

    if any(fav.planet_id == planet_id for fav in user.favorite_planets):
        return jsonify({'msg': 'El planeta ya está en favoritos'}), 400

    favorite = FavoritePlanets(user_id=user.id, planet_id=planet.id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({'msg': 'Planeta agregado a favoritos'}), 200


@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404

    favorite = FavoritePlanets.query.filter_by(user_id=user.id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({'msg': f'El planeta con id {planet_id} no está en favoritos'}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'msg': 'Planeta eliminado de favoritos'}), 200




                #Starships

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
    return jsonify({'msg': 'Starship not found'}), 404

@app.route('/favorite/<int:user_id>/starship/<int:starship_id>', methods=['POST'])
def add_favorite_starship(user_id, starship_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404

    starship = Starships.query.get(starship_id)
    if not starship:
        return jsonify({'msg': f'La starship con id {starship_id} no existe'}), 404

    if any(fav.starship_id == starship_id for fav in user.favorite_starships):
        return jsonify({'msg': 'La starship ya está en favoritos'}), 400

    favorite = FavoriteStarships(user_id=user.id, starship_id=starship.id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({'msg': 'Starship agregada a favoritos'}), 200

@app.route('/favorite/<int:user_id>/starship/<int:starship_id>', methods=['DELETE'])
def delete_favorite_starship(user_id, starship_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404

    favorite = FavoriteStarships.query.filter_by(user_id=user.id, starship_id=starship_id).first()
    if not favorite:
        return jsonify({'msg': f'La nave espacial con id {starship_id} no está en favoritos'}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'msg': 'Nave espacial eliminada de favoritos'}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
