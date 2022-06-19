import pytest
import json
from app.wsgi import app

with open('tests/testdata.json', 'r') as file:
    data = json.loads(file.read())


@pytest.mark.parametrize('host, path', data['safedomains']+data['unsafedomains'])
def test_format(setup_data, host, path):
    with app.test_client() as test_client:
        res = test_client.get(f'/api/1/{host}/{path}')
        data = json.loads(res.data)
        assert 'data' in data.keys()
        assert 'is_safe' in data.keys()
        assert data['is_safe'] != ''
        assert data['is_safe'] == True or data['is_safe'] == False
        assert 'url' in data['data'].keys()
        if data['is_safe']:
            assert data['data']['url'] == f'http://{host}/{path}'
        else:
            assert data['data']['url'] == 'Forbidden'
