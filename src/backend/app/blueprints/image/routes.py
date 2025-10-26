import os
from pathlib import Path

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

from ..main.models import Image
from . import image_bp
from werkzeug.utils import secure_filename
from datetime import datetime

WALLPAPERS_DIR = Path("src/frontend/wallpapers")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg',}


def allowed_file(filename):
    """Проверка  расширений файла."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@image_bp.route("/api/image", methods=["GET", "POST"])
def image_add():
    if request.method == "POST":
        # Проверка на наличие файла
        if "file" not in request.files:
            flash("Файл не выбран", "error")
            return redirect(request.url)

        file = request.files["file"]
        #Проверка на корректность имени
        if file.filename == '':
            flash("Файл не выбран", "error")
            return redirect(request.url)
        
          # Проверка на разрешенные форматы
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = WALLPAPERS_DIR / filename

            WALLPAPERS_DIR.mkdir(parents=True, exist_ok=True)
            file.save(filepath)

            
            new_image = Image(filename=filename, uploaded_at=datetime.utcnow())
            db.session.add(new_image) 
            db.session.commit() 

            flash("Изображение успешно загружено и сохранено в базе данных!", "success")
            return redirect(url_for("image_bp.image_add"))
        else:
            flash("Недопустимый формат файла", "error")
            return redirect(request.url)

    return render_template("image_add.html")


       # flash("Image add")
       # return redirect(url_for("image_bp.image_add"))
   # return render_template("image_add.html")
