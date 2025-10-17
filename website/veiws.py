from flask import Blueprint

views  = Blueprint("views", __name__) # Create a Blueprint instance for views which means this file will handle routing

@views.route("/") # Define a route for the home page
def home():# Define the home function to handle requests to the home page views will return "Home Page"
    return "<h1>Home Page</h1>"