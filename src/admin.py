import os
from flask_admin import Admin
from models import db, User, Characters, FavoriteCharacters, Planets, FavoritePlanets, Starships, FavoriteStarships
from flask_admin.contrib.sqla import ModelView


class UsersModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'email', 'password', 'is_active','favorite_characters', 'favorite_planets', 'favorite_starships']


class CharactersModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'height', 'weigth', 'favorite_by']


class FavoriteCharactersModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'user', 'characters_id', 'character']


class PlanetsModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'population','climate', 'diameter', 'favorite_by']


class FavoritePlanetsModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'user', 'planet_id', 'planet']


class StarshipsModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'model','starship_class', 'passengers', 'favorite_by']


class FavoriteStarshipsModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'user', 'starship_id', 'starship']


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin

    admin.add_view(UsersModelView(User, db.session))

    admin.add_view(CharactersModelView(Characters, db.session))
    admin.add_view(FavoriteCharactersModelView(FavoriteCharacters, db.session))

    admin.add_view(PlanetsModelView(Planets, db.session))
    admin.add_view(FavoritePlanetsModelView(FavoritePlanets, db.session))

    admin.add_view(StarshipsModelView(Starships, db.session))
    admin.add_view(FavoriteStarshipsModelView(FavoriteStarships, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
