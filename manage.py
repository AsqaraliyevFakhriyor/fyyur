from locale import currency
from sqlite3 import dbapi2
from models import db
from flask import current_app

app = current_app()
db.init_app(app)

db.create_all()