"""Simple model loader stub for testing endpoints.

Replace the internals with actual model loading (torch.hub, ultralytics, etc.)
when integrating a real YOLO model.
"""
_LOADED_MODEL = None


def load_yolo_model(path=None):
    global _LOADED_MODEL
    # In real implementation, load weights and return model object
    _LOADED_MODEL = {'name': 'yolo-stub', 'path': path}
    return _LOADED_MODEL


def get_loaded_model():
    return _LOADED_MODEL


def unload_model():
    global _LOADED_MODEL
    _LOADED_MODEL = None
