import pytest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.routes import app, r


class MockRedis:
    def __init__(self):
        self.data = {}

    def incr(self, key):
        self.data[key] = self.data.get(key, 0) + 1

    def get(self, key):
        return self.data.get(key, 0)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    global r
    app.view_functions['vote'].__globals__['r'] = MockRedis()
    app.view_functions['results'].__globals__['r'] = MockRedis()

    with app.test_client() as client:
        yield client


def test_glosowanie(client):
    rv = client.post('/api/vote', json={'option': 'Python'})
    assert rv.status_code == 200
    assert b"Oddano glos na: Python" in rv.data


def test_nieprawidlowa_opcja(client):
    rv = client.post('/api/vote', json={'option': 'Inne'})
    assert rv.status_code == 400