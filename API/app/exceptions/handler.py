"""Handles application's errors and exceptions"""


from flask import jsonify
from app.models import Blacklist
from werkzeug.exceptions import default_exceptions


def init_app(app):
    """JSONify all the HTTP errors"""
    for code in default_exceptions.keys():
        @app.errorhandler(code)
        def handle_error(ex):
            """Returns the http exception with its error code
            and message.
            """
            return jsonify({'message': str(ex)}), code


def init_jwt(jwt):
    """Handles the JWT blacklists for logged out users."""
    @jwt.token_in_blacklist_loader
    def check_token_in_blacklist(decrypted_token):
        return Blacklist.query.filter_by(
                    token=decrypted_token['jti']).first() is not None
