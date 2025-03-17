import pytest 
from app import app 
 
@pytest.fixture 
def client(): 
    app.config['TESTING'] = True 
    with app.test_client() as client: 
        yield client 
 
def test_home_page(client): 
    response = client.get('/') 
    assert response.status_code == 200 
    assert b'Telefon' in response.data
 
def test_add_to_cart(client): 
    response = client.get('/add/1') 
    assert response.status_code == 200
    assert b'Telefon sepete eklendi' in response.data