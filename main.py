from website import create_app # Import the create_app function from the website folder

app = create_app() # Create an instance of the Flask application

if __name__ == '__main__': # only run the app if this file is executed directly
    app.run(debug=True) # Run the Flask application in debug mode
