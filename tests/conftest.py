
import pytest
from app.wsgi import app
from app.db.models.malware import Malware
from sqlalchemy import exc


@pytest.fixture
def setup_data():
    paths = [
        ["mdomain", "mpath"],
        ["malwaredomain:2000", ""],
        ["malware.domain.com", "?path=malware"],
        ["malware.domain.com", ""]
    ]
    for host, path in paths:
        data = {'url': f"{host}/{path}"}
        fetch = app.session.query(Malware).filter(
            Malware.url == f"{data['url']}",
            Malware.dtime.is_not(None)
        ).all()
        if len(fetch) != 0:
            fetch = fetch[0]
            setattr(fetch, 'dtime', None)
        else:
            newdata = Malware(url=data['url'], dtime=None)
            app.session.add(newdata)
        try:
            app.session.commit()

        except exc.IntegrityError:
            app.session.rollback()
        except Exception as e:
            app.session.rollback()
