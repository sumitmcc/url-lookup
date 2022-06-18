import json

import pytest
from app.wsgi import app
from app.db.models.malware import Malware


@pytest.fixture
def setup_data():
    paths = [
        ('mdomain', 'mpath'),
        ('malwaredomain:2000', ''),
        ('malware.domain.com', "?path=malware"),
        ('malware.domain.com', "")
    ]
    for host, path in paths:
        data = app.session.query(Malware).filter(
            Malware.host == f"{host}",
            Malware.path == f"{path}"
        ).all()
        if len(data) != 0:
            data = data[0]
            setattr(data, 'dtime', None)
            app.session.commit()
        else:
            data = Malware(host=host, path=path, dtime=None)
            app.session.add(data)
            app.session.commit()

