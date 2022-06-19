import logging

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level=logging.INFO)

DB_NAME = "arboretum_dev"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:postgres@localhost:5432/{DB_NAME}"

db = SQLAlchemy(app)
ma = Marshmallow(app)
