import os
from environ import Env

env = Env()
env.read_env(".env")


SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = env.bool("DEBUG")
# Connect to the database

# TRACK modificitaion
SQLALCHEMY_TRACK_MODIFICATIONS = env.bool("SQLALCHEMY_TRACK_MODIFICATIONS")

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = env.str("SQLALCHEMY_DATABASE_URI")
