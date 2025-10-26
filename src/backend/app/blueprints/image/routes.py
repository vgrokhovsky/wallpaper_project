import os
from datetime import datetime
from pathlib import Path

from app.db import db_object as db
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from ..main.models import Image
from . import image_bp

WALLPAPERS_DIR = Path("src/frontend/wallpapers")
ALLOWED_EXTENSIONS = (
    "png",
    "jpg",
    "jpeg",
)


def allowed_file(filename):
    """Проверка  расширений файла."""
    return "." in filename and filename.rsplit(".", 1)[-1].lower() in ALLOWED_EXTENSIONS


@image_bp.route("/api/image", methods=["GET", "POST"])
def image_add():
    if request.method == "POST":
        file = request.files.get("file")

        # Проверка на наличие файла
        if not file:
            flash("Файл не выбран", "error")
            return redirect(request.url)

        # Проверка на корректность имени !!!
        if file.filename in '\/:*?"<>|+"':
            flash('Имя файла не должно содержать, \/:*?"<>|+"', "error")
            return redirect(request.url)

        # Проверка на разрешенные форматы
        if not allowed_file(file.filename):
            flash("Недопустимый формат файла", "error")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filepath = os.path.join(WALLPAPERS_DIR, filename)

        WALLPAPERS_DIR.mkdir(parents=True, exist_ok=True)  # !!!
        file.save(filepath)

        # user_id !!!
        new_image = Image(filename=filename, user_id=user_id, orientation=orientation)
        try:
            db.session.add(new_image)
            db.session.commit()
            flash(
                "Изображение успешно загружено и сохранено в базе данных!",
                "success",
            )
            return redirect(url_for("image_bp.image_add"))
        except Exception as e:
            print("error", e)
        finally:
            db.session.close()

    return render_template("image_add.html")

    # flash("Image add")
    # return redirect(url_for("image_bp.image_add"))


# return render_template("image_add.html")
