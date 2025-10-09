import os
from pathlib import Path

from flask import Blueprint, jsonify, request

from . import main_bp
from .models import Category, Colors, Image, Keywords

WALLPAPERS_DIR = Path("src/frontend/wallpapers")


@main_bp.route("/api/wallpapers", methods=["GET"])
def get_wallpapers():
    try:
        # /api/wallpapers?category=cat
        # /api/wallpapers?orientation=vertical
        category = request.args.get("category", default=None)
        orientation = request.args.get("orientation", default=None)
        color = request.args.get("colors", default=None)
        keyword = request.args.get("keywords", default=None)

        filters = {}
        if category:
            category_id = Category.get_id_by_name(category)
            filters["category_id"] = category_id
        if orientation:
            filters["orientation"] = orientation
        if color:
            color_id = Colors.get_id_by_name(color)
            filters["color_id"] = color_id
        if keyword:
            keyword_id = Keywords.get_id_by_name(keyword)
            filters["keyword_id"] = keyword_id

        images = Image.get_images_by_filter(filters)

        wallpapers = [f"wallpapers/{image.name}" for image in images]

        # wallpapers = [
        #     f"wallpapers/{filename}"
        #     for filename in os.listdir(WALLPAPERS_DIR)
        #     if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
        # ]
        return jsonify({"wallpapers": wallpapers}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
