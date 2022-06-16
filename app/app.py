from flask import json, request
from app import create_app
from app.db.models.malware import Malware


app = create_app()


@app.get('/api/1/<_hostname_port>/<_path_query>')
def is_malware(_hostname_port, _path_query):
    data = app.session.query(Malware).filter(
        Malware.url == f"{_hostname_port}/{_path_query}"
    ).all()
    if len(data) == 0:
        response = {
            "url": f"http://{_hostname_port}/{_path_query}",
            "is_safe": True,
            "data": {
                "host": f"{_hostname_port}".split(':')[0],
                "port": f"{_hostname_port}".split(':')[1] if len(f"{_hostname_port}".split(':')) > 1 else "",
                "path": f"{_path_query}"
            }
        }
    else:
        response = {
            "url": f"",
            "is_safe": False,
            "data": {
                "host": f"{_hostname_port}".split(':')[0],
                "port": f"{_hostname_port}".split(':')[1] if len(f"{_hostname_port}".split(':')) > 1 else "",
                "path": f"{_path_query}"
            }
        }
    return f"{json.dumps(response)}", 200


@app.post('/api/1/add')
def add_malware():
    data = request.get_json()
    print(data)
    try:
        _hostname_port = data['hostname_port']
        _path_query = data['path_query']
    except KeyError:
        return "BAD Request: POST request expects hostname_port and path_query keys", 400
    data = Malware(url=f"{_hostname_port}/{_path_query}")
    app.session.add(data)
    app.session.commit()
    return f"{data}", 201

@app.get('/')
def index():
    print("Test")
    return json.dumps("Edited"), 200
