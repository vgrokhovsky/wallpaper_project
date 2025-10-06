import os
from pathlib import Path

from flask import Blueprint, jsonify, request
from models import Category, Colors, Image, Keywords

from . import main_bp

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

        images_page = Image.get_images_by_filter(filters, page=page, per_page=per_page)

        wallpapers = [f"wallpapers/{image.filename}" for image in images_page.items]

       
        return jsonify({
            "wallpapers": wallpapers,
            "page": images_page.page,  
            "total_pages": images_page.pages, 
            "total_items": images_page.total  
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500