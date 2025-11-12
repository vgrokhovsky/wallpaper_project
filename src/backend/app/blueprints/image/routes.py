import os
from datetime import datetime
from pathlib import Path

from app.db import db_object as db
from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.utils import secure_filename

from ..main.models import Colors, Image
from . import image_bp
from .forms import ImageForm

WALLPAPERS_DIR = Path("src/frontend/wallpapers")
ALLOWED_EXTENSIONS = (
    "png",
    "jpg",
    "jpeg",
)


def allowed_file(filename):
    """Проверка расширений файла."""
    print(filename.rsplit(".", 1)[-1].lower())
    print(filename.rsplit(".", 1)[-1].lower() in ALLOWED_EXTENSIONS)
    return (
        "." in filename
        and filename.rsplit(".", 1)[-1].lower() in ALLOWED_EXTENSIONS
    )


@image_bp.route("/image", methods=["GET", "POST"])
def image_add():
    user_id = None
    form = ImageForm()
    if form.validate_on_submit() or request.method == "POST":
        if form.validate_on_submit():
            file = form.file.data
        else:
            file = form.request.data
        # Проверка на наличие файла
        if not file:
            flash("Файл не выбран", "error")
            return redirect(request.url)

        # Проверка на корректность имени !!!
        if file.filename in ':*?"<>|+':
            flash('Имя файла не должно содержать, :*?<>|+"', "error")
            return redirect(request.url)

        print("имя верное")
        # Проверка на разрешенные форматы
        if not allowed_file(file.filename):
            flash("Недопустимый формат файла", "error")
            return redirect(request.url)

        print("формат верный")
        filename = secure_filename(file.filename)  # !!! Случайное значение
        filepath = os.path.join(WALLPAPERS_DIR, filename)

        WALLPAPERS_DIR.mkdir(parents=True, exist_ok=True)  # !!!
        file.save(filepath)
        color_by_image = Image.extract_main_color(filepath)
        hex_color = Colors.rgb_to_hex(color_by_image)

        color = Colors.get_id_by_name(hex_color)

        if not color:
            distance = Colors.color_distance_simple(color_by_image)
            color = Colors(name=hex_color, distance=distance)
            color_id = color.id
            color.add()

        new_image = Image(
            name=filename,
            user_id=user_id,
            orientation=form.orientation.data,
            colors=color_id,
        )
        try:
            db.session.add(new_image)
            db.session.commit()
            flash(
                "Изображение успешно загружено и сохранено в базе данных!",
                "success",
            )
            print("добавил в базу")
            return redirect(url_for("image_bp.image_add"))
        except Exception as e:
            print("error", e)
        finally:
            db.session.close()

    return render_template("image_add.html", form=form)

    # flash("Image add")
    # return redirect(url_for("image_bp.image_add"))


# return render_template("image_add.html")
