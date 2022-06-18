from flask import Flask
from app.db import db, migrate
from app.db import config
from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy.orm import sessionmaker
import sqlalchemy


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    engine = sqlalchemy.create_engine(config.DATABASE_CONNECTION_URI)
    session_factory = sessionmaker(bind=engine)
    _scoped_session = flask_scoped_session(session_factory, flask_app)
    flask_app.session = _scoped_session
    flask_app.app_context().push()
    db.init_app(flask_app)
    db.create_all()
    migrate.init_app(flask_app, db)
    return flask_app