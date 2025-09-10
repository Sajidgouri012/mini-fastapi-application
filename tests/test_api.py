from fastapi.testclient import TestClient
from main import app
import os, models, database, shutil

client = TestClient(app)

def setup_function():
    # reset DB file before each test
    try:
        os.remove('test.db')
    except FileNotFoundError:
        pass
    models.Base.metadata.create_all(bind=database.engine)

def teardown_function():
    try:
        os.remove('test.db')
    except FileNotFoundError:
        pass

def test_create_and_get_item():
    setup_function()
    resp = client.post('/items/', json={'title': 'alpha', 'description': 'first'})
    assert resp.status_code == 201
    data = resp.json()
    assert data['title'] == 'alpha'
    item_id = data['id']

    getr = client.get(f'/items/{item_id}')
    assert getr.status_code == 200
    assert getr.json()['title'] == 'alpha'

    # test list and pagination
    resp2 = client.post('/items/', json={'title': 'beta', 'description': 'second'})
    assert resp2.status_code == 201
    lst = client.get('/items/?limit=1&offset=0')
    assert lst.status_code == 200
    assert len(lst.json()) == 1

    teardown_function()
