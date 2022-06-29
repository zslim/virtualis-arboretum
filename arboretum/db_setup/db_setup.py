import json
import logging
import os
import time

import marshmallow

from arboretum import models
from arboretum.app import app

LOGGER = logging.getLogger(__name__)


def deserialize_data_from_json(file_path, schema_class):
    with open(file_path) as json_file:
        file_content = json.load(json_file)
    schema = schema_class(many=True)
    try:
        objects = schema.load(file_content)
    except marshmallow.exceptions.ValidationError as e:
        LOGGER.warning(f"Validation error while loading {file_path} according to {schema_class}")
        raise e
    return objects


def load_init_data():
    init_data_directory = "init_data"
    # Order: referenced table first, referencing one later
    init_data_files_schemas = {"families.json": models.PlantFamilySchema, "life_forms.json": models.PlantLifeFormSchema,
                               "life_form_subcategories.json": models.LifeFormSubcategorySchema,
                               "plants.json": models.PlantSchema}

    data_objects = []
    for file_name, schema in init_data_files_schemas.items():
        file_path = os.path.join(init_data_directory, file_name)
        table_data = deserialize_data_from_json(file_path, schema)
        data_objects += table_data
    return data_objects


def get_user_confirmation():
    LOGGER.warning("Entering the danger zone.")
    time.sleep(0.5)
    database_name = app.config.get("SQLALCHEMY_DATABASE_URI").split("/")[-1]
    confirm_input = input(f"You are about to drop every table from the '{database_name}' database. "
                          f"Please type the name of the database if you are sure about this. ")
    if confirm_input.lower() != database_name:
        LOGGER.error(f"Drop not confirmed (you typed: '{confirm_input}'). Aborting.")
        raise RuntimeError(f"Aborting drop of database {database_name}.")


def setup_database():
    LOGGER.info("Setting up tables")
    models.db.drop_all()
    models.db.create_all()

    LOGGER.info("Loading data from files")
    init_data = load_init_data()
    models.db.session.add_all(init_data)
    models.db.session.commit()


def setup_main():
    LOGGER.info("Starting")
    get_user_confirmation()
    setup_database()
    LOGGER.info("Done")


if __name__ == '__main__':
    setup_main()
