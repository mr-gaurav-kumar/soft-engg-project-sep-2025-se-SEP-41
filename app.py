# Main app code
# Importing required libraries
from flask import Flask
from database import db
from models import *
from resources import api

from config import LocalDevelopmentConfig
from flask_security import Security, SQLAlchemyUserDatastore # these are the API with many useful methods to configure user and role model
from flask_security import hash_password
from werkzeug.security import generate_password_hash
from datetime import datetime, date

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(LocalDevelopmentConfig) #Sqlite connection
#     db.init_app(app) # Flask app is connected to db
#     api.init_app(app)
#     app.app_context().push() 
#     return app

# # Call the setup function
# app = create_app()

# # whenever we want to do DB operations in app.py, we need to create the app context

# with app.app_context():
#     db.create_all()

#     db.session.commit()


# from routes import *

# if __name__ == '__main__':
#     app.run()



def create_app(config_class=LocalDevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    api.init_app(app)

    # Import routes so they register with THIS app instance
    from routes import setup_routes
    setup_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)