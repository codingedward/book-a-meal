from app.models import User
from flask import jsonify, abort, make_response
from flask_jwt_extended import  jwt_required, get_jwt_identity


@jwt_required
def default_auth(**kwargs):
    """We use this empty function to as a preprocessor in JWT restless
    in order to include the @jwt_required decorator. That way, we
    can gaurd our API endpoints.
    """
    pass


@jwt_required
def caterer_auth(**kwargs):
    """This is similar to caterer_auth with the extra requirement of a user 
    being a caterer
    """
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    if not current_user.is_caterer():
        abort(
            make_response( 
                jsonify({'message': 'Unauthorized access to a non-caterer'}), 
                401
            )
        )
