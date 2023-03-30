import pytest
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_homepage_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200

def test_signin_returns_200(client):
    response = client.get('/signin')
    assert response.status_code == 200

def test_signup_returns_200(client):
    response = client.get('/signup')
    assert response.status_code == 200

def test_stocks_returns_200(client):
    response = client.get('/stocks')
    assert response.status_code == 200
