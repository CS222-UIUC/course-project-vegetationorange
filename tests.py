import pytest
from server import app
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# basic endpoint tests
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

# /stock endpoint lookup tests
def test_incomplete_stock_lookup_returns_400(client):
    response1 = client.post('/stocks', data={})
    response2 = client.post('/stocks', data={'random_key': 'random_val'})
    assert response1.status_code == 400 and response2.status_code == 400

def test_real_stock_lookup_returns_200(client):
    response = client.post('/stocks', data={'stock_symbol': "TSLA"})
    assert response.status_code == 200

def test_fake_stock_lookup_returns_202(client):
    response = client.post('/stocks', data={'stock_symbol': "garbage"})
    assert response.status_code == 202