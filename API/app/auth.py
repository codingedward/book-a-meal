import json
from app.models import Blacklist, User, UserType 
from app.validators import validate_user, AuthorizationError
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)


auth = Blueprint('auth', __name__)


@jwt_required
def customer_auth(**kwargs):
    """ 
    We use this empty function to as a preprocessor in JWT restless
    in order to include the @jwt_required decorator. That way, we
    can gaurd our API endpoints.
    """
    pass

@jwt_required
def caterer_auth(**kwargs):
    """ 
    This is similar to caterer_auth with the extra requirement of a user 
    being a caterer
    """
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    if not current_user.is_caterer():
        raise AuthorizationError('Unauthorized access to a non-caterer')


@auth.route('/api/v1/auth/signup', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({'message': 'Request should be JSON'}), 400

    try:
        validate_user()
    except ValidationError as err:
        return jsonify({'errors': [str(err)]}), 400

    user = User(
        username=request.json['username'],
        email=request.json['email'],
        password=request.json['password']
    )
    user.save()
    return jsonify({'message': 'Successfully registered'}), 201

@auth.route('/api/v1/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'message': 'Request should be JSON'}), 400

    if not request.json.get('email'):
        return jsonify({'errors': ['Email is required']}), 400
    if not request.json.get('password'):
        return jsonify({'errors': ['Password is required']}), 400

    user = User.query.filter_by(email=request.json['email']).first()
    if not user or not user.validate_password(request.json['password']):
        return jsonify({'errors': ['Invalid credentials']}), 400

    access_token = create_access_token(identity=request.json['email'])
    return jsonify(access_token=access_token), 200


@auth.route('/api/v1/auth/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist = Blacklist(token=jti)
    blacklist.save()
    return jsonify({'message': 'Successfully logged out.'}), 200
