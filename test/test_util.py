import pytest

from arboretum import util


@pytest.mark.parametrize(["test_input", "expected"], [
    ("postgres://", "postgresql://"),
    ("http://postgres://ok", "http://postgres://ok")
])
def test_correct_database_uri_prefix(test_input, expected):
    actual = util.correct_database_uri_prefix(test_input)
    assert actual == expected


@pytest.mark.parametrize(["url", "expected"], [
    ("postgresql://postgres:postgres@localhost:5432/arboretum_test",
     "postgresql://postgres:postgres@localhost:5432/arboretum_test"),
    ("postgres://postgres:postgres@localhost:5432/arboretum_test",
     "postgresql://postgres:postgres@localhost:5432/arboretum_test"),
    ("postgres://postgresql:postgres@host:port/db", "postgresql://postgresql:postgres@host:port/db")
])
def test_read_database_uri(monkeypatch, url, expected):
    monkeypatch.setattr("os.getenv", lambda k: url)
    actual = util.read_database_uri()
    assert actual == expected


def test_read_database_uri_raises(monkeypatch):
    monkeypatch.setattr("os.getenv", lambda k: None)
    with pytest.raises(RuntimeError):
        util.read_database_uri()
