'''
Tests for jwt flask app.
'''
import os
import random
import json
import pytest

import app

BARISTA_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhXZmJYMkFrM0lfWWxkVk42R18tTyJ9.eyJpc3MiOiJodHRwczovL2Rldi1zcDR4N2ZqYTQ0czFhYXlyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzZkMGJkYjhhZDM5OTI4MmMxMWY5YTYiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjgwMDAvIiwiaWF0IjoxNjY4NjQ2MjIxLCJleHAiOjE2Njg2NTM0MjEsImF6cCI6IkNuYzNmZUdkNWVmRUJkQ1dycDhKZzBEbjdldlpCZXIwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6ZHJpbmtzLWRldGFpbCJdfQ.N5FZk8pU3qsG-p2b2898NuM_OEwXVq9NYaKQ9KvRe2mYPwwD--nK8_Z-7I4cIpD7D98QSjAisymyDl5nv45lFGhu-VxvBn8SaHSlFFVMPH3xHCbQE_d41JhkMCqStbfHA6cJxRB8AGJbWjcBu4h5g04MPDt-9JeMgJ87Z_htjWvDGbiye7RHwL1GDvNx6I1f4wlipIowmCJ8JqXH1TVhcsSEW1DAWg5IhlnXSuf_RrjGnWpNn3wK8rrr4YDUxWwLvgmYFuq1USvdzZzPHKHWgzQrz91CmWeRID6nXKLk3b9otv4fTL4SnEk53cHbMvJm_6KEILACGs7nlnDiHNpvXQ'
MANAGER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhXZmJYMkFrM0lfWWxkVk42R18tTyJ9.eyJpc3MiOiJodHRwczovL2Rldi1zcDR4N2ZqYTQ0czFhYXlyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzZkMGMxYWNmOTFkMmE3NmU5NDRlNmYiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjgwMDAvIiwiaWF0IjoxNjY4NjQ2MTQyLCJleHAiOjE2Njg2NTMzNDIsImF6cCI6IkNuYzNmZUdkNWVmRUJkQ1dycDhKZzBEbjdldlpCZXIwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y3VzdG9tZXJzIiwiZGVsZXRlOmRyaW5rcyIsImdldDpjdXN0b21lciIsImdldDpjdXN0b21lcnMiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmN1c3RvbWVycyIsInBhdGNoOmRyaW5rcyIsInBvc3Q6Y3VzdG9tZXJzIiwicG9zdDpkcmlua3MiXX0.JpOQamO_xv5dV0ux5o5ua3xLbrg56f_wQ4unIuldcsV9iYejrC8KYZnGnixoKFtQrFCCbq7_YWmf2xzWWdAh7W-G4x7O8kvkhWM8gE4-mjmOCOZDY7poGyAornmVnNcmIfGODmFugrHs5QpyiRZkTOFlW-r-JLNJrfiO_ykFmHCvaVVfNXrd15zATUGTN6woXm_py3UoeCLo1OuKP02fgWSY9C7ISWbsfoCW9VaaqfLFg3288OgYKA0uFU4OD0MUpdbVCVF28t_PUO0x6vEwJjVXMi_j5RmOdoQTfc5f8u8J_s9_H2ldCbaBQNt9xO8n0YFoZg4AdUvUj1JeSoExPQ'
DATABASE_URL = "postgres://nuyukgsdjomluk:bdbb2db3e9e25f44369f41b0de5c599d68b4bbc8106344991ef0d94a0f4fb8f7@ec2-3-227-68-43.compute-1.amazonaws.com:5432/dd934k39b1vj7u"
AUTH0_DOMAIN = "dev-sp4x7fja44s1aayr.us.auth0.com"
API_AUDIENCE = "http://localhost:8000/"


@pytest.fixture
def client():
    os.environ['DATABASE_URL'] = DATABASE_URL
    os.environ['AUTH0_DOMAIN'] = AUTH0_DOMAIN
    os.environ['API_AUDIENCE'] = API_AUDIENCE
    app.app.config['TESTING'] = True
    client = app.app.test_client()

    yield client


def test_success_get_customers(client):
    headers = {'Authorization': f'Bearer { MANAGER_TOKEN }'}
    response = client.get('/customers', headers=headers)

    assert response.status_code == 200
    assert response.json is not None

def test_unauthorized_get_customers(client):
    headers = {'Authorization': f'Bearer { BARISTA_TOKEN }'}
    response = client.get('/customers', headers=headers)

    assert response.status_code == 401
    assert response.json is not None

def test_success_get_drinks(client):
    headers = {'Authorization': f'Bearer { MANAGER_TOKEN }'}
    response = client.get('/drinks', headers=headers)

    assert response.status_code == 200
    assert response.json is not None

def test_unauthorized_post_drinks(client):
    headers = {'Authorization': f'Bearer { BARISTA_TOKEN }'}
    response = client.post('/drinks', headers=headers)

    assert response.status_code == 401
    assert response.json is not None

def test_success_post_drinks(client):
    title = f"Water {random.randint(0, 100)}"
    body = {
        "title": title,
        "recipe": {
            "name": "Water",
            "color": "blue",
            "parts": 1
        }
    }
            
    headers = {'Authorization': f'Bearer { MANAGER_TOKEN }'}
    response = client.post('/drinks', data=json.dumps(body), headers=headers,
                           content_type='application/json')

    assert response.status_code == 200
    drink = response.json['drinks']
    assert drink['title'] == title
    assert drink['recipe']["name"] == "Water"