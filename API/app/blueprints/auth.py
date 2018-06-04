import string
import random
from app.models import User, Blacklist
from app.mail import (
    email_verification,
    password_reset
)
from app.validators import Valid
from flask_restless import ProcessingException
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)


auth = Blueprint('auth', __name__)


@auth.route('/api/v1/auth/signup', methods=['POST'])
def register():
    try:
        Valid.user()
    except ProcessingException as err:
        return jsonify({'message': err.description}), 400

    user = User(
        username=request.json['username'],
        email=request.json['email'],
        password=request.json['password']
    )
    user.save()
    user.token = str(user.id).join(random.choices(
        string.ascii_letters + string.digits, k=60))
    user.save()

    email_verification(
        token=user.token,
        recipient=request.json['email']
    )
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 201


@auth.route('/api/v1/auth/verify/<string:token>', methods=['GET'])
def verify(token):
    user = User.query.filter_by(token=token).first()
    if not user:
        return jsonify({
            'errors': ['Could not find a user for the token provided.'] 
        }), 400
    user.token = ''
    user.save()
    return jsonify({
        'message': 'Successfully verified your email address.'
    })


@auth.route('/api/v1/auth/login', methods=['POST'])
def login():
    if not request.json.get('email'):
        return jsonify({'errors': ['Email is required']}), 400
    if not request.json.get('password'):
        return jsonify({'errors': ['Password is required']}), 400

    user = User.query.filter_by(email=request.json['email']).first()
    if not user or not user.validate_password(request.json['password']):
        return jsonify({'errors': ['Invalid credentials']}), 400

    if user.token: 
        return jsonify({
            'errors': ['This account is not verified. Please verify your
                       email address.'] 
        }), 400

    access_token = create_access_token(identity=request.json['email'])
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200

@auth.route('/api/v1/auth/password-reset', methods=['POST'])
def reset_password():
    if not request.json.get('email'):
        return jsonify({'errors': ['Email is required']}), 400
    if not request.json.get('password'):
        return jsonify({'errors': ['Password is required']}), 400
    if not request.json.get('confirm_password'):
        return jsonify({'errors': ['Password confirmation is required']}), 400


@auth.route('/api/v1/auth/get', methods=['GET'])
@jwt_required
def get_user():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200


@auth.route('/api/v1/auth/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist = Blacklist(token=jti)
    blacklist.save()
    return jsonify({'message': 'Successfully logged out.'}), 200

