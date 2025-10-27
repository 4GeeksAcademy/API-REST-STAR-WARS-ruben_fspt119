from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorite_characters: Mapped[list['FavoriteCharacters']] = relationship(back_populates='user')
    favorite_planets: Mapped[list["FavoritePlanets"]] = relationship(back_populates='user')
    favorite_starships: Mapped[list["FavoriteStarships"]] = relationship(back_populates='user')

    def __repr__(self):
        return f'Usuario {self.email}'
    
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active
        }


class Characters(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    height: Mapped[int] = mapped_column(Integer)
    weigth: Mapped[int] = mapped_column(Integer)
    favorite_by: Mapped[list['FavoriteCharacters']] = relationship(back_populates='character')

    def __repr__(self):
        return f'Personaje {self.name}'
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height,
            'weigth': self.weigth
        }

class FavoriteCharacters(db.Model):
    __tablename__ = 'favorite_characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='favorite_characters')
    characters_id: Mapped[int] = mapped_column(ForeignKey('characters.id'), nullable=False)
    character: Mapped['Characters'] = relationship(back_populates='favorite_by')

    def __repr__(self):
        return f'Al usuario {self.user_id} le gusta el personaje {self.characters_id}'
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'character': self.character.serialize()
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    population: Mapped[int] = mapped_column(Integer)
    climate: Mapped[str] = mapped_column(String(50))
    diameter: Mapped[int] = mapped_column(Integer)
    favorite_by: Mapped[list["FavoritePlanets"]] = relationship(back_populates='planet')

    def __repr__(self):
        return f'Planeta {self.name}'
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'population': self.population,
            'climate': self.climate,
            'diameter': self.diameter
        }

class FavoritePlanets(db.Model):
    __tablename__ = 'favorite_planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user: Mapped["User"] = relationship(back_populates='favorite_planets')
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable=False)
    planet: Mapped["Planets"] = relationship(back_populates='favorite_by')

    def __repr__(self):
        return f'Al usuario {self.user_id} le gusta el planeta {self.planet_id}'
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet': self.planet.serialize()
        }

class Starships(db.Model):
    __tablename__ = 'starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    model: Mapped[str] = mapped_column(String(100))
    starship_class: Mapped[str] = mapped_column(String(50))
    passengers: Mapped[int] = mapped_column(Integer)
    favorite_by: Mapped[list["FavoriteStarships"]] = relationship(back_populates='starship')

    def __repr__(self):
        return f'Starship {self.name}'
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'starship_class': self.starship_class,
            'passengers': self.passengers
        }

class FavoriteStarships(db.Model):
    __tablename__ = 'favorite_starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user: Mapped["User"] = relationship(back_populates='favorite_starships')
    starship_id: Mapped[int] = mapped_column(ForeignKey('starships.id'), nullable=False)
    starship: Mapped["Starships"] = relationship(back_populates='favorite_by')
   
    def __repr__(self):
        return f'Al usuario {self.user_id} le gusta el starship {self.starship_id}'
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'starship': self.starship.serialize()
        }