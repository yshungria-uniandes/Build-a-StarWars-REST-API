
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "favorites": [f.serialize() for f in self.favorites]
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    favorites = db.relationship('Favorite', backref='people', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(20))
    terrain = db.Column(db.String(20))
    favorites = db.relationship('Favorite', backref='planet', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id
        }

