import base64
import io


def decode_base64_image(b64_string):
    """Decode a base64 image (optionally data URL) and return bytes.

    Raises ValueError on invalid input.
    """
    if not b64_string:
        raise ValueError('empty string')

    if ',' in b64_string:
        # data:image/png;base64,....
        b64_string = b64_string.split(',', 1)[1]

    try:
        return base64.b64decode(b64_string)
    except Exception as e:
        raise ValueError('invalid base64') from e

