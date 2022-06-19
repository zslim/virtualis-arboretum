import json
import logging
import os
import time

import marshmallow

import app_init
import models

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
                               "weed_categories.json": models.WeedCategorySchema, "plants.json": models.PlantSchema}

    data_objects = []
    for file_name, schema in init_data_files_schemas.items():
        file_path = os.path.join(init_data_directory, file_name)
        table_data = deserialize_data_from_json(file_path, schema)
        data_objects += table_data
    return data_objects


def get_user_confirmation():
    LOGGER.warning("Entering the danger zone.")
    time.sleep(0.5)
    confirm_input = input(f"You are about to drop every table from the '{app_init.DB_NAME}' database. "
                          f"Are you sure? (y/n) ")
    if confirm_input.lower() != "y":
        LOGGER.error(f"Drop not confirmed (you typed: '{confirm_input}'). Aborting.")
        raise RuntimeError(f"Aborting drop of database '{app_init.DB_NAME}'.")


def setup_database():
    LOGGER.info("Setting up tables")
    models.db.drop_all()
    models.db.create_all()

    LOGGER.info("Loading data from files")
    init_data = load_init_data()
    models.db.session.add_all(init_data)
    models.db.session.commit()


if __name__ == '__main__':
    LOGGER.info("Starting")
    get_user_confirmation()
    setup_database()
    LOGGER.info("Done")
