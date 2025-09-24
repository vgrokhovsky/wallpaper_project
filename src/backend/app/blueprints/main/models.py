from datetime import datetime
from app.db import db_object as db

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    upload_date = db.Column(db.DateTime, default=datetime.now)
    views_count = db.Column(db.Integer, default=0)

    user = db.relationship('User', back_populates='images')
    favorites = db.relationship('Favorite', back_populates='image')

class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', back_populates='favorites')
    image = db.relationship('Image', back_populates='favorites')