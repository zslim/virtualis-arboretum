import logging

from flask import Flask

from arboretum import models
from arboretum import util
from arboretum.endpoints import error_handlers, rest, swagger

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level=logging.INFO)


def create_app():
    application = Flask("arboretum")
    application.config["SQLALCHEMY_DATABASE_URI"] = util.read_database_uri()
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    application.register_blueprint(rest.blueprint)
    application.register_blueprint(swagger.blueprint)
    application.register_blueprint(error_handlers.blueprint)

    models.db.init_app(application)
    models.ma.init_app(application)

    return application


app = create_app()
app.app_context().push()

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5050,
        debug=True
    )
