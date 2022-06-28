import os


def correct_database_uri_prefix(db_uri):
    wrong_prefix = "postgres://"
    right_prefix = "postgresql://"
    if db_uri.startswith(wrong_prefix):
        right_url = db_uri.replace(wrong_prefix, right_prefix, 1)
        return right_url
    else:
        return db_uri


def read_database_uri():
    db_uri_key = "DATABASE_URL"
    db_uri = os.getenv(db_uri_key)
    if db_uri is None:
        raise RuntimeError("Database URI not specified")
    else:
        corrected_uri = correct_database_uri_prefix(db_uri)
        return corrected_uri
