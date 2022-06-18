from app.wsgi import app

def teardown_module(module):
    app.session.execute("delete from urllookup;")
    app.session.commit()