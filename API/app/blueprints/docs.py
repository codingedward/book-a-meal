from flask import Blueprint, send_from_directory


documentation = Blueprint('documentation', __name__)


@documentation.route('/')
def docs():
    return send_from_directory('../docs', 'index.html')
