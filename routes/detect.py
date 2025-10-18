from flask import request, jsonify, current_app
from . import bp
from utils.helpers import decode_base64_image


@bp.route('/detect', methods=['POST'])
def detect():
    """Accepts JSON with either:
    - `image`: base64 data URL or raw base64 string
    - `image_url`: remote image URL

    Returns a template response that matches typical YOLO output:
    { detections: [{label, confidence, bbox: [x1,y1,x2,y2]}], meta: {...} }
    """
    payload = request.get_json(silent=True) or {}

    image_b64 = payload.get('image')
    image_url = payload.get('image_url')

    if not image_b64 and not image_url:
        return jsonify({'error': 'missing image or image_url'}), 400

    # In integration: decode image and pass to inference pipeline
    if image_b64:
        try:
            image_bytes = decode_base64_image(image_b64)
        except Exception as e:
            return jsonify({'error': 'invalid base64 image', 'details': str(e)}), 400
    else:
        image_bytes = None

    # TODO: call the model inference (synchronous or async) and return real detections
    # Example placeholder response follows:
    example = {
        'detections': [
            {'label': 'person', 'confidence': 0.97, 'bbox': [12, 34, 56, 78]},
            {'label': 'dog', 'confidence': 0.88, 'bbox': [120, 40, 200, 180]}
        ],
        'meta': {
            'source': 'stub',
            'inference_time_ms': 12
        }
    }

    return jsonify(example)
