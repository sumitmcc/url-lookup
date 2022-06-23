import json
from app.wsgi import app
from app.db.models.malware import Malware

with open('tests/testdata.json', 'r') as file:
    data = json.loads(file.read())

adds = [f'{x[0]}/{x[1]}' for x in data['unsafedomains']]
addone = [f'{x[0]}/{x[1]}' for x in data['addone']]


def teardown_module(module):
    stmt = Malware.__table__.delete().where(Malware.url.in_(adds+addone+data['addmany']))
    app.session.execute(stmt)
    app.session.commit()
