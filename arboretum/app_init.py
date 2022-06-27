import logging
import os

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level=logging.INFO)

# Debug mode base url config
HOST = "127.0.0.1"
PORT = 5050

app = Flask("virtualis_arboretum", static_folder="arboretum/static", template_folder="arboretum/templates")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", default="Database URI not specified")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
