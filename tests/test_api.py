"""
Simple API Tests for Key-Value Store
"""

import pytest
from backend.kv_api.app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()


def test_put_and_get(client):
    """Test basic PUT and GET functionality"""
    response = client.put('/put/kv/test_key',
                         json={'value': 'hello world'})
    assert response.status_code == 200
    
    response = client.get('/get/kv/test_key')
    assert response.status_code == 200
    data = response.get_json()
    assert data['value'] == 'hello world'


def test_put_number(client):
    """Test storing a number"""
    response = client.put('/put/kv/number',
                         json={'value': 42})
    assert response.status_code == 200
    
    response = client.get('/get/kv/number')
    data = response.get_json()
    assert data['value'] == 42


def test_put_object(client):
    """Test storing a JSON object"""
    test_obj = {'name': 'John', 'age': 30}
    
    response = client.put('/put/kv/user',
                         json={'value': test_obj})
    assert response.status_code == 200
    
    response = client.get('/get/kv/user')
    data = response.get_json()
    assert data['value'] == test_obj


def test_missing_key(client):
    """Test getting a key that doesn't exist"""
    response = client.get('/get/kv/nonexistent')
    assert response.status_code == 200
    data = response.get_json()
    assert data['value'] is None or data['response'] == 'error'
