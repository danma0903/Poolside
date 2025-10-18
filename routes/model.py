from flask import jsonify, request
from . import bp
from utils.model_loader import load_yolo_model, get_loaded_model, unload_model


@bp.route('/model/load', methods=['POST'])
def model_load():
    """Load a model into memory. Payload may include `path` or `name`."""
    data = request.get_json(silent=True) or {}
    path = data.get('path')
    model = load_yolo_model(path=path)
    return jsonify({'status': 'loaded', 'model': model})


@bp.route('/model', methods=['GET'])
def model_info():
    """Return info about the currently loaded model (if any)."""
    model = get_loaded_model()
    if not model:
        return jsonify({'loaded': False}), 200
    return jsonify({'loaded': True, 'model': model})


@bp.route('/model/unload', methods=['POST'])
def model_unload():
    unload_model()
    return jsonify({'status': 'unloaded'})
