from flask import Blueprint


common = Blueprint('common', __name__)

from app.common import common

