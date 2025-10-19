import os
from pathlib import Path

<<<<<<< HEAD
from flask import jsonify, request
=======
from flask import Blueprint, jsonify, request
<<<<<<< HEAD
>>>>>>> b8b8ad3 (09.10.2025)
=======
>>>>>>> a3fbf787ef700e8e22515d6752c7cdf5e66c7d89

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
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)

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

        images_page = Image.get_images_by_filter(
            page=page, per_page=per_page, **filters
        )

        wallpapers = [f"wallpapers/{image.filename}" for image in images_page.items]

        return (
            jsonify(
                {
                    "wallpapers": wallpapers,
                    "page": images_page.page,
                    "total_pages": images_page.pages,
                    "total_items": images_page.total,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
