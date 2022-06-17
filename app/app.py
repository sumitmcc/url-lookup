from datetime import datetime
from flask import json, request
from app import create_app
from app.db.models.malware import Malware

app = create_app()


@app.get('/api/1/<_hostname_port>/<_path_query>')
@app.get('/api/1/<_hostname_port>/')
def is_malware(_hostname_port, _path_query=""):
    additional_query = request.query_string
    if additional_query:
        _path_query = f"{_path_query}?{additional_query.decode('utf-8')}"
    data = app.session.query(Malware).filter(
        Malware.host == f"{_hostname_port}",
        Malware.path == "",
        Malware.dtime.is_(None)
    ).all()
    resp = {'host': _hostname_port, 'path': _path_query}
    if len(data) != 0:
        response = Malware._set_return_value(resp, False)
        return f"{json.dumps(response)}", 200

    data = app.session.query(Malware).filter(
        Malware.host == f"{_hostname_port}",
        Malware.path == f"{_path_query}",
        Malware.dtime.is_(None)
    ).all()
    if len(data) == 0:
        response = Malware._set_return_value(resp, True)
        response['url'] = f"http://{_hostname_port}/{_path_query}"
    else:
        response = Malware._set_return_value(resp, False)
    return f"{json.dumps(response)}", 200


@app.post('/api/1/add')
def add_malware():
    data = request.get_json()
    try:
        _hostname_port = data['hostname_port']
        _path_query = data['path_query']
    except KeyError:
        return "BAD Request: POST request expects hostname_port and path_query keys", 400
    data = app.session.query(Malware).filter(
        Malware.host == f"{_hostname_port}",
        Malware.path == f"{_path_query}"
    ).all()
    resp = {'host': _hostname_port, 'path': _path_query}
    response = Malware._set_return_value(resp, False)
    if len(data) != 0:
        data = data[0]
        setattr(data, 'dtime', None)
        app.session.commit()
        return f"{json.dumps(response)}", 200
    else:
        data = Malware(host=_hostname_port, path=_path_query, dtime=None)
        app.session.add(data)
        app.session.commit()

    return f"{json.dumps(response)}", 201


@app.delete('/api/1/delete')
def delete_malware():
    data = request.get_json()
    try:
        _hostname_port = data['hostname_port']
        _path_query = data['path_query']
    except KeyError:
        return "BAD Request: DELETE request expects hostname_port and path_query keys", 400
    data = app.session.query(Malware).filter(
        Malware.host == f"{_hostname_port}",
        Malware.path == f"{_path_query}",
        Malware.dtime.is_(None)
    ).all()
    if not data:
        return json.dumps({'hostname_port': _hostname_port, 'path_query': _path_query}), 200
    data = data[0]
    setattr(data, 'dtime', data.dtime or datetime.now())
    app.session.commit()
    return json.dumps({'hostname_port': _hostname_port, 'path_query': _path_query}), 200

