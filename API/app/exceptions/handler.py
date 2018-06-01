from flask import abort, make_response, jsonify, Blueprint
from app.models import Blacklist
from flask_jwt_extended import get_raw_jwt
from werkzeug.exceptions import HTTPException, default_exceptions


def init_app(app):
    # jsonify http errors
    for code in default_exceptions.keys():
        @app.errorhandler(code)
        def handle_error(ex):
            return jsonify({'message': str(ex)}), code


def init_jwt(jwt):
    @jwt.token_in_blacklist_loader
    def check_token_in_blacklist(decrypted_token):
        return Blacklist.query.filter_by(
                    token=decrypted_token['jti']).first() is not None
