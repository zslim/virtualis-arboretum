from arboretum import models


def create_response_body_deleted(_id, name):
    body = {"message": f"Plant (id: {_id}, name: {name}) deleted."}
    return body


def delete_row(model_class, row_id):
    row_to_delete = model_class.query.get(row_id)
    models.db.session.delete(row_to_delete)
    models.db.session.commit()
    response_body = create_response_body_deleted(row_id, row_to_delete.scientific_name)
    return response_body


def insert_row(schema_class, payload):
    schema = schema_class()
    row_object = schema.load(payload)
    models.db.session.add(row_object)
    models.db.session.commit()
    return schema.jsonify(row_object)
