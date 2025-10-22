import os
from pathlib import Path

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

from ..main.models import Image
from . import image_bp

WALLPAPERS_DIR = Path("src/frontend/wallpapers")


@image_bp.route("/api/image", methods=["GET", "POST"])
def image_add():
    if request.method == "POST":
        # Проверка на наличие файла
        if "file" not in request.files:
            flash("Файл не выбран", "error")
            return redirect(request.url)

        file = request.files["file"]

        flash("Image add")
        return redirect(url_for("image_bp.image_add"))
    return render_template("image_add.html")
