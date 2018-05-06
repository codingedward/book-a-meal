from flask_jwt_extended import get_raw_jwt
from werkzeug.exceptions import HTTPException, default_exceptions
from app.validators import AuthorizationError



def errors_handler(app):
    # jsonify http errors
    for code in default_exceptions.keys():
        @app.errorhandler(code)
        def handle_error(ex):
            return jsonify({'message': str(ex)}), code

    # jsonify authorization error
    @app.errorhandler(AuthorizationError)
    def handle_authorization_error(err):
        return jsonify({'message': str(err)}), 401


def blacklist_handler(jwt):
    @jwt.token_in_blacklist_loader
    def check_token_in_blacklist(decrypted_token):
        return Blacklist.query.filter_by(
                    token=get_raw_jwt()['jti']).first() is not None
