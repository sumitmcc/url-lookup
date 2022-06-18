from flask import Blueprint

bp = Blueprint('malware', __name__)
from app.routes import malware