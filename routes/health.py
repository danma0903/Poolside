from flask import jsonify
from . import bp


@bp.route('/health', methods=['GET'])
def health():
    """Basic health endpoint to check service and model status."""
    # In integration, expand to check model loaded, memory, GPU, etc.
    return jsonify({'ok': True, 'model_loaded': False})
