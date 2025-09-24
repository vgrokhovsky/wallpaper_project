from flask import Blueprint, render_template, jsonify
import os
from pathlib import Path

from . import main_bp

WALLPAPERS_DIR = Path('src/frontend/wallpapers')

@main_bp.route('/api/wallpapers', methods=['GET'])
def get_wallpapers():
    try:
        wallpapers = [
            f'wallpapers/{filename}'
            for filename in os.listdir(WALLPAPERS_DIR)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
        ]
        return jsonify({'wallpapers': wallpapers}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500