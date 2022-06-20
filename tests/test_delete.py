import json

import pytest
from app.wsgi import app

with open('tests/testdata.json', 'r') as file:
    data = json.loads(file.read())


@pytest.mark.parametrize('url', data['deleteone'])
def test_delete_existing(setup_data, url):
    body = {'url': url}
    with app.test_client() as test_client:
        res = test_client.delete('api/1/delete', json=body)
        assert res.status_code == 201
        assert json.loads(res.data)['is_safe'] == True
        assert json.loads(res.data)['data']['url'] == "http://"+url

