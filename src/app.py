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
from models import db, User
#from models import Person

from models import People, Planet, Favorite

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

# # generate sitemap with all your endpoints
# @app.route('/')
# def sitemap():
#     return generate_sitemap(app)

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

    # return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([p.serialize() for p in people])

@app.route('/people', methods=['POST'])
def create_person():
    data = request.get_json()
    new_person = People(name=data['name'], birth_year=data.get('birth_year'), gender=data.get('gender'))
    db.session.add(new_person)
    db.session.commit()
    return jsonify(new_person.serialize()), 201

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person:
        return jsonify(person.serialize())
    return jsonify({"error": "Person not found"}), 404

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify(planet.serialize())
    return jsonify({"error": "Planet not found"}), 404

# Adicionalmente, necesitamos crear los siguientes endpoints para que podamos tener usuarios y favoritos en nuestro blog:

# [GET] /users Listar todos los usuarios del blog.
# [GET] /users/favorites Listar todos los favoritos que pertenecen al usuario actual.
# [POST] /favorite/planet/<int:planet_id> Añade un nuevo planet favorito al usuario actual con el id = planet_id.
# [POST] /favorite/people/<int:people_id> Añade un nuevo people favorito al usuario actual con el id = people_id.
# [DELETE] /favorite/planet/<int:planet_id> Elimina un planet favorito con el id = planet_id.
# [DELETE] /favorite/people/<int:people_id> Elimina un people favorito con el id = people_id.

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users])

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    
    if len(favorites) > 0:
        return jsonify([f.serialize() for f in favorites])
    return jsonify({"error": "favorites not found"}), 404

@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)
    if user and planet:
        new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(new_favorite.serialize()), 201
    return jsonify({"error": "User or planet not found"}), 404

@app.route('/favorite/user/<int:user_id>/people/<int:people_id>', methods=['POST'])
def add_people_favorite(user_id, people_id):
    user = User.query.get(user_id)
    people = People.query.get(people_id)
    if user and people:
        new_favorite = Favorite(user_id=user_id, people_id=people_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(new_favorite.serialize()), 201
    return jsonify({"error": "User or People not found"}), 404

@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(user_id, planet_id):
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"success": "Favorite deleted"}), 200
    return jsonify({"error": "Favorite not found"}), 404

@app.route('/favorite/user/<int:user_id>/people/<int:people_id>', methods=['DELETE'])
def delete_people_favorite(user_id, people_id):
    favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"success": "Favorite deleted"}), 200
    return jsonify({"error": "Favorite not found"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
