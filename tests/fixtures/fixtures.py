import os

import pytest
from preparation.data_base import DataBase, Books, Lines

src_to_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'books.db')  # pragma: no cover


@pytest.fixture
def empty_database():
    test_db = DataBase()
    yield test_db
    test_db.session.close()
    os.remove(src_to_db)


@pytest.fixture
def populated_database():
    src_to_test_text = TEST_DATA_DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'test_data/test_text.txt')
    test_title = "test title - + = !@#$%^&*()!№;%:?*()"
    test_author = "test author 'd"
    test_lang = "RU"
    test_db = DataBase()

    test_book = Books(src=src_to_test_text, title=test_title, author=test_author, lang=test_lang)
    test_string = 'В середине августа, перед рождением молодого месяца, вдруг наступили отвратительные погоды, какие так свойственны северному побережью Черного моря.'

    test_line = Lines(line=test_string, books_id=test_book.id)

    test_db.session.add(test_book)
    test_db.session.add(test_line)
    test_db.session.commit()

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
