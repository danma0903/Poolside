from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'key'

    from .veiws import views # Import the views blueprint
    from .auth import auth   # Import the auth blueprint

    app.register_blueprint(views, url_prefix="/") # Register the views blueprint with the app
    app.register_blueprint(auth, url_prefix="/")  # Register the auth blueprint with the app url_prefix means all routes defined in the blueprint will be prefixed with this string


    return app