import flask_sqlalchemy
from flask_migrate import Migrate
db = flask_sqlalchemy.SQLAlchemy()
migrate = Migrate()
