from datetime import datetime

from app.db import db_object as db

category_image = db.Table(
    "category_image",
    db.Column(
        "image_id",
        db.Integer,
        db.ForeignKey("images.id"),
        primary_key=True,
    ),
    db.Column(
        "category_id",
        db.Integer,
        db.ForeignKey("categories.id"),
        primary_key=True,
    ),
)


colors_image = db.Table(
    "colors_image",
    db.Column(
        "image_id",
        db.Integer,
        db.ForeignKey("images.id"),
        primary_key=True,
    ),
    db.Column(
        "colors_id",
        db.Integer,
        db.ForeignKey("colors.id"),
        primary_key=True,
    ),
)


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    orientation = db.Column(db.String(32), nullable=False)  # vertical, horizontal
    upload_date = db.Column(db.DateTime, default=datetime.now)
    views_count = db.Column(db.Integer, default=0)
    last_view = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="images")
    favorites = db.relationship("Favorite", back_populates="image")
    categories = db.relationship("Category", secondary=category_image, backref="images")
    colors = db.relationship("Colors", secondary=colors_image, backref="images")

    # GET
    def get_images_by_filter(self):
        pass

    def get_random_images(self):
        pass

    # CRUD
    def add(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass


class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship("User", back_populates="favorites")
    image = db.relationship("Image", back_populates="favorites")


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    images = db.relationship("Image", secondary="category_image", backref="categories")

    # CRUD
    def add(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass


class Colors(db.Model):
    __tablename__ = "colors"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
    )
    images = db.relationship(
        "Image",
        secondary=colors_image,
        back_populates="colors",
    )

    def add(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass
