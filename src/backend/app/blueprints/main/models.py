import random
from datetime import datetime

from app.db import db_object as db
from sqlalchemy.exc import SQLAlchemyError

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


keywords_image = db.Table(
    "keywords_image",
    db.Column(
        "image_id",
        db.Integer,
        db.ForeignKey("images.id"),
        primary_key=True,
    ),
    db.Column(
        "keywords_id",
        db.Integer,
        db.ForeignKey("keywords.id"),
        primary_key=True,
    ),
)


class BaseModel(db.Model):
    __abstract__ = True

    # CRUD
    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error adding image: {e}")
            return False
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting image: {e}")
            return False
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating image: {e}")
            return False
        finally:
            db.session.close()

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.query.get(id)
        except SQLAlchemyError as e:
            raise Exception(f"Ошибка при получении {str(e)}")

    @classmethod
    def get_all(cls):
        try:
            return cls.query.all()
        except SQLAlchemyError as e:
            raise Exception(f"Ошибка при получении {str(e)}")


class Image(BaseModel):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    orientation = db.Column(db.String(32), nullable=False)  # vertical, horizontal
    upload_date = db.Column(db.DateTime, default=datetime.now)
    views_count = db.Column(db.Integer, default=0)
    last_view = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="images")
    favorites = db.relationship("Favorite", back_populates="image")
    categories = db.relationship("Category", secondary=category_image, backref="images")
    colors = db.relationship("Colors", secondary=colors_image, backref="images")
    keywords = db.relationship("Keywords", secondary=keywords_image, backref="images")

    # GET

    @classmethod
    def get_images_by_filter(cls, **filters):
        query = cls.query

        # for filter_name in filters.keys():
        #     pass

        if "category_id" in filters:
            query = query.join(category_image).filter(
                category_image.c.category_id == filters["category_id"]
            )

        if "color_id" in filters:
            query = query.join(colors_image).filter(
                colors_image.c.colors_id == filters["color_id"]
            )

        if "orientation" in filters:
            pass

        if "keywords" in filters:
            pass

        return query.all()

    def get_random_images(self, limit=20):
        # images = db.session.query(Image).all()
        # return random.sample(images, min(limit, len(images)))
        images = db.session.query(Image).order_by(db.func.random()).limit(limit).all()
        return images


class Favorite(BaseModel):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship("User", back_populates="favorites")
    image = db.relationship("Image", back_populates="favorites")


class Category(BaseModel):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    images = db.relationship("Image", secondary="category_image", backref="categories")


class Colors(BaseModel):
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
