from flask import Flask, request, jsonify, Blueprint, render_template

app = Flask(__name__, template_folder='website/templates', static_folder='website/static')
# Register API blueprint (adds routes under /api/*)
from routes import bp as api_bp
app.register_blueprint(api_bp)
#app.register_blueprint(, url_prefix='/')
veiws  = Blueprint('veiws',__name__)
app.register_blueprint(veiws)


@app.route('/')
def home():
    return render_template("index.html")

@app.route("/get-user/<user_id>") #endpoint to get user information by user_id
def get_user(user_id):
    user_data = {# mock user data
        "user_id": user_id,
        "name": "John Doe",
        "email": "jdoe@example.com"
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra
    return jsonify(user_data)


@app.route("/create-user", methods=["POST"]) #endpoint to create a new user
def create_user():
    user_info = request.get_json()
    response = { # mock response for user creation
        "message": "User created successfully",
        "user": user_info
    }
    return jsonify(response), 201







if __name__ == "__main__": #if this file is run directly, start the Flask app
    app.run(debug=True)