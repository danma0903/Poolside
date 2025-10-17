from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

# Import route modules to register handlers on the blueprint
from . import detect, model, health, external_api  # noqa: F401
