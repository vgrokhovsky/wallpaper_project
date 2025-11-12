import math
import random
from datetime import datetime

from app.db import db_object as db
from colorthief import ColorThief
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

    # CRUD
    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
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
    def get_id_by_name(cls, name):
        try:
            return cls.query.get(name)
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

    name = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    orientation = db.Column(
        db.String(32), nullable=False
    )  # vertical, horizontal
    upload_date = db.Column(db.DateTime, default=datetime.now)
    views_count = db.Column(db.Integer, default=0)
    last_view = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="images")
    favorites = db.relationship("Favorite", back_populates="image")
    categories = db.relationship(
        "Category", secondary=category_image, back_populates="images"
    )
    colors = db.relationship(
        "Colors", secondary=colors_image, back_populates="images"
    )
    keywords = db.relationship(
        "Keywords", secondary=keywords_image, back_populates="images"
    )

    @staticmethod
    def save_image(img, img_name):
        pass

    @staticmethod
    def extract_main_color(file):
        color_thief = ColorThief(file)
        dominant_color = color_thief.get_color(quality=1)
        return dominant_color

    # GET

    @classmethod
    def get_images_by_filter(cls, page=1, per_page=10, **filters):
        query = cls.query

        if "category_id" in filters:
            query = query.join(category_image).filter(
                category_image.c.category_id == filters["category_id"]
            )

        if "color_id" in filters:
            query = query.join(colors_image).filter(
                colors_image.c.colors_id == filters["color_id"]
            )

        if "orientation" in filters:
            query = query.filter(Image.orientation == filters["orientation"])

        if "keyword_id" in filters:
            query = query.join(keywords_image).filter(
                keywords_image.c.keyword_id == filters["keyword_id"]
            )

        return query.paginate(page, per_page, error_out=False)

    def get_random_images(self, limit=20):
        images = (
            db.session.query(Image)
            .order_by(db.func.random())
            .limit(limit)
            .all()
        )
        return images


class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship("User", back_populates="favorites")
    image = db.relationship("Image", back_populates="favorites")


class Category(BaseModel):
    __tablename__ = "categories"

    images = db.relationship(
        "Image",
        secondary=category_image,
        back_populates="categories",
    )

    name_ru = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
    )


class Colors(BaseModel):
    __tablename__ = "colors"

    images = db.relationship(
        "Image",
        secondary=colors_image,
        back_populates="colors",
    )
    distance = db.Column(db.Float, nullable=False)

    @classmethod
    def color_distance_simple(cls, color):
        white = (255, 255, 255)

        # Проверяем, что введенный цветвалидный RGB
        if not all(0 <= c <= 255 for c in color):
            raise ValueError(
                "Значения цвета должны быть в диапазоне от 0 до 255"
            )

        # Вычисляем расстояние
        distance = math.sqrt(
            (color[0] - white[0]) ** 2
            + (color[1] - white[1]) ** 2
            + (color[2] - white[2]) ** 2
        )
        return distance

    @classmethod
    def rgb_to_hex(cls, rgb_color):
        r, g, b = rgb_color
        return f"#{r:02x}{g:02x}{b:02x}"

    def hex_to_rgb(self, hex_color):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b)

    @classmethod
    def get_image_by_color_distance(cls, distance):
        colors = cls.query.filter(cls.distance == distance)
        images_list = []
        for color in colors:
            images_list += color.images
        return images_list


class Keywords(BaseModel):
    __tablename__ = "keywords"

    images = db.relationship(
        "Image",
        secondary=keywords_image,
        back_populates="keywords",
    )
    name_ru = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
    )
