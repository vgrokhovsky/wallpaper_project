from flask import Blueprint

image_bp = Blueprint("images", __name__, template_folder="templates")

from . import routes
