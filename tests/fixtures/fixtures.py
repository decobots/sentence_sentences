import os

import pytest

from preparation.data_base import DataBase

test_db_name = 'test_db'
db_name_with_extension = f"{test_db_name}.db"


@pytest.fixture
def empty_table():
    test_db = DataBase(test_db_name)
    yield test_db
    test_db.session.close()
    os.remove(db_name_with_extension)
