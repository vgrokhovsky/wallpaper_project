from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from  auth.models import User, Image, Category, Colors, Favorite
from db import db


def configure_admin(app):
    admin = Admin(app, name=' Администратор', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Image, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Colors, db.session))
    admin.add_view(ModelView(Favorite, db.session))