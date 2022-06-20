import json
import pytest
from app.wsgi import app

with open('tests/testdata.json', 'r') as file:
    data = json.loads(file.read())


@pytest.mark.parametrize("host, path",data['addone'])
def test_create(host, path):
    url = f"{host}/{path}"
    body = {'url': url}
    with app.test_client() as test_client:
        res = test_client.post('api/1/add', json=body)
        assert res.status_code == 201
        assert json.loads(res.data)['is_safe'] == False
        assert json.loads(res.data)['data']['url'] == 'Forbidden'


def test_createmany():
    body = {'malware_list': data['addmany']}
    with app.test_client() as test_client:
        res = test_client.post('api/1/createmany', json=body)
        assert res.status_code == 201
        response_items = []
        for item in json.loads(res.data)['data']:
            response_items.append(item['url'])
            assert item['dtime'] is None
            assert isinstance(item['id'], int)
        for item in data['addmany']:
            assert item in response_items


def test_createmany_duplicate():
    body = {'malware_list': data['addmany']}
    with app.test_client() as test_client:
        res = test_client.post('api/1/createmany', json=body)
        assert res.status_code == 201
        response_items = []
        assert response_items == []
