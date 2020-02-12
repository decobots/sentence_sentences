import pytest
from falcon import testing

from falcon_app.app import create


@pytest.fixture()
def client():
    # Assume the hypothetical `myapp` package has a function called
    # `create()` to initialize and return a `falcon.API` instance.
    return testing.TestClient(create("sqlite:///tests/test_data/falcon.db"))


def test_get_message(client):
    result = client.simulate_get('/quotes')
    assert result.json == ['В', 'середине', 'августа,', 'перед', 'рождением', 'молодого', 'месяца,', 'вдруг',
                           'наступили', 'отвратительные', 'погоды,', 'какие', 'так', 'свойственны', 'северному',
                           'побережью', 'Черного', 'моря.']


def test_option_message(client):
    result = client.simulate_options('/quotes')
    assert result.status == '200 OK'
