from flask import Blueprint

info_type = Blueprint('info_type', __name__)
from . import views
