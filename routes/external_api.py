import requests
from flask import jsonify
from . import bp


@bp.route('/external/test', methods=['GET'])
def external_test():
    """Template for calling an external API (keeps it isolated for testing).

    This endpoint simply proxies a GET to httpbin.org/get and returns a sanitized result.
    """
    try:
        resp = requests.get('https://httpbin.org/get')
        data = resp.json()
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 502

    return jsonify({'ok': True, 'external': data})
