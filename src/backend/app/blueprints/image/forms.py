from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

from ..main.models import Category, Keywords


class ImageForm(FlaskForm):
    file = FileField("Загрузить файл", validators=[DataRequired()])
    categories = SelectMultipleField(
        "Категоря",
        choices=[
            ("cat", "кот"),
            ("nature", "природа"),
        ],
        # choices = get_all_category(Category),
        validators=[DataRequired()],
    )
    orientation = SelectField(
        "Ориентация",
        choices=[
            ("vertical", "вертикальная"),
            ("horizontal", "горизонтальная"),
        ],
        validators=[DataRequired()],
    )
    keywords = SelectMultipleField(
        "Ключевые слова",
        choices=[
            ("cat", "кот"),
            ("nature", "природа"),
        ],
        # choices = get_all_category(Keywords),
        validators=[DataRequired()],
    )

    @staticmethod
    def get_all_category(model_class):
        items = model_class.get_all()
        result = []
        for item in items:
            result.append((item.name, item.name_ru))
        return result

    submit = SubmitField("Отравить")
