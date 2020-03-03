import pytest
import os
from falcon import testing

from falcon_app.app import create
from preparation.data_base import Books, Lines

src_to_test_text = TEST_DATA_DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'test_data/test_text.txt')

src_to_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests", 'books.db')  # pragma: no cover
test_title = "test title - + = !@#$%^&*()!№;%:?*()"
test_author = "test author 'd"
test_lang = "RU"


@pytest.fixture()
def client(populated_database):
    # Assume the hypothetical `myapp` package has a function called
    # `create()` to initialize and return a `falcon.API` instance.

    return testing.TestClient(create(populated_database.engine.url))


def test_get_message(client):
    result = client.simulate_get('/quotes')
    assert result.json == 'В середине августа, перед рождением молодого месяца, вдруг наступили отвратительные погоды, какие так свойственны северному побережью Черного моря.'


def test_option_message(client):
    result = client.simulate_options('/quotes')
    assert result.status == '200 OK'
