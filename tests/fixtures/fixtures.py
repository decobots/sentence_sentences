import os

import pytest
from preparation.data_base import DataBase

src_to_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'books.db')  # pragma: no cover


@pytest.fixture
def empty_database():
    test_db = DataBase()
    yield test_db
    test_db.session.close()
    os.remove(src_to_db)


@pytest.fixture()
def global_variable():
    key = "TEST_VARIABLE"
    value = "TEST_VALUE"
    os.environ[key] = value
    yield key, value
    os.environ.pop(key)
