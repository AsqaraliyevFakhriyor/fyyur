import os

SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = os.env.get("DEBUG")
# Connect to the database

# TRACK modificitaion
SQLALCHEMY_TRACK_MODIFICATIONS = os.env.get("SQLALCHEMY_TRACK_MODIFICATIONS")

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = os.env.get("DATABASE_URL")
