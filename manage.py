from locale import currency
from sqlite3 import dbapi2
from models import db
from flask import current_app

app = current_app
db.init_app(app)
with app.app_context():
    db.create_all()