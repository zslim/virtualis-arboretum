import logging

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from swagger_gen import swagger

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level=logging.INFO)

DB_NAME = "arboretum_dev"
HOST = "127.0.0.1"
PORT = 5050

app = Flask("virtualis_arboretum")
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:postgres@localhost:5432/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


def init_swagger(flask_app):
    swagger_instance = swagger.Swagger(
        app=flask_app,
        title="Virtuális Arborétum",
        version="0.0.1",
        license_name="MIT License",
        license_url="https://mit-license.org/"
    )
    return swagger_instance
