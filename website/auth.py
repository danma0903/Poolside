from flask import Blueprint

auth  = Blueprint("auth", __name__) # Create a Blueprint instance for views which means this file will handle routing

@auth.route("/login") # Define a route for the login page
def login():# Define the login function to handle requests to the login page auth will return "Login Page"
    return "<h1>Login Page</h1>"

@auth.route("/signup") # Define a route for the signup page
def signup():# Define the signup function to handle requests to the signup page auth will return "
    return "<h1>Signup Page</h1>"

@auth.route("/logout") # Define a route for the logout page note: you need to have the route the same as the function name
def logout():# Define the logout function to handle requests to the logout page auth will return "Logout Page"
    return "<h1>Logout Page</h1>"