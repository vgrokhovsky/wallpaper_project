import os
from pathlib import Path

from flask import Blueprint, jsonify, request

from . import main_bp

WALLPAPERS_DIR = Path("src/frontend/wallpapers")


@main_bp.route("/api/wallpapers", methods=["GET"])
def get_wallpapers():
    try:
        # /api/wallpapers?category=cat
        # /api/wallpapers?orientation=vertical
        category = request.args.get("category", default=None)
        orientation = request.args.get("orientation", default=None)

        if category:
            pass
        if orientation:
            pass

        wallpapers = [
            f"wallpapers/{filename}"
            for filename in os.listdir(WALLPAPERS_DIR)
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
        ]
        return jsonify({"wallpapers": wallpapers}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
