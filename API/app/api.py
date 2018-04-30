from app.model import BAM, UserType
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)
from flask import Blueprint, jsonify, request
from passlib.hash import bcrypt


api = Blueprint('api', __name__)
bam = BAM()
blacklist = set()


"""
Authentication Routes

"""

def is_caterer():
    current_user = bam.get_user_by_email(get_jwt_identity())
    return current_user['role'] == UserType.CATERER

@api.route('/api/v1/auth/signup', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({'message': 'Request should be JSON'}), 400

    fails, errors = bam.validate_user_fails(request.json)
    if fails:
        return jsonify({'errors': errors}), 400

    request.json['role'] = UserType.CUSTOMER
    return jsonify(bam.post_user(request.json)), 201


@api.route('/api/v1/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'message': 'Request should be JSON'}), 400

    if not request.json.get('email'):
        return jsonify({'errors': ['Email is required']}), 400
    if not request.json.get('password'):
        return jsonify({'errors': ['Password is required']}), 400

    user = bam.get_internal_user_by_email(request.json['email'])
    if not user or not bcrypt.verify(request.json['password'], user['password']):
        return jsonify({'errors': ['Invalid credentials']}), 400

    access_token = create_access_token(identity=request.json['email'])
    return jsonify(access_token=access_token), 200


@api.route('/api/v1/auth/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({'msg': 'Successfully logged out.'}), 200


"""
Meals Routes

"""


@api.route('/api/v1/meals', methods=['POST'])
@jwt_required
def meals():
    if not is_caterer():
        return jsonify({
            'errors': ['Unauthorized access to non-caterer']}), 401

    if not request.is_json:
        return jsonify({
            'errors': ['Request should be JSON']}), 400

    fails, errors = bam.validate_meal_fails(request.json)
    if fails:
        return jsonify({'errors': errors}), 400
    return jsonify(bam.post_meal(request.json)), 201


@api.route('/api/v1/meals', methods=['GET'])
def meals_get():
    return jsonify({'num_results': len(bam.meals),
                    'objects': list(bam.get_meals().values())})


@api.route('/api/v1/meals/<int:id>', methods=['DELETE', 'PATCH'])
@jwt_required
def meal_modify(id):
    if not is_caterer():
        return jsonify({
            'errors': ['Unauthorized access to non-caterer']}), 401

    if request.method == 'DELETE':
        if id not in bam.meals.keys():
            return jsonify({'errors': ['Not Found']}), 404
        bam.delete_meal(id)
        return jsonify({'message': 'Successfully deleted'}), 204


    elif request.method == 'PATCH':
        if not request.is_json:
            return jsonify({'errors': ['Request should be JSON']}), 400

        if id not in bam.meals:
            return jsonify({'errors': ['Not Found']}), 404

        fails, errors = bam.validate_meal_fails(request.json)
        if fails:
            return jsonify({'errors': errors}), 400
        bam.put_meal(request.json, id)
        return jsonify({'message': 'Successfully updated'}), 200


@api.route('/api/v1/meals/<int:id>', methods=['GET'])
def meal(id):
    if id not in bam.meals.keys():
        return jsonify({'errors': ['Not Found']}), 404
    return jsonify(bam.get_meal(id)), 200


"""
Menus Routes

"""


@api.route('/api/v1/menus', methods=['POST'])
@jwt_required
def menus():
    if not is_caterer():
        return jsonify({
            'errors': ['Unauthorized access to non-caterer']}), 401

    if not request.is_json:
        return jsonify({
            'errors': ['Request should be JSON']}), 400

    fails, errors = bam.validate_menu_fails(request.json)
    if fails:
        return jsonify({'errors': errors}), 400
    return jsonify(bam.post_menu(request.json)), 201


@api.route('/api/v1/menus', methods=['GET'])
def menus_get():
    return jsonify({'num_results': len(bam.menus),
                    'objects': list(bam.get_menus().values())})


@api.route('/api/v1/menus/<int:id>', methods=['PATCH', 'DELETE'])
@jwt_required
def menu_modify(id):
    if not is_caterer():
        return jsonify({
            'errors': ['Unauthorized access to non-caterer']}), 401

    if request.method == 'DELETE':
        if id not in bam.menus.keys():
            return jsonify({'errors': ['Not Found']}), 404
        bam.delete_menu(id)
        return jsonify({'message': 'Successfully deleted'}), 204

    elif request.method == 'PATCH':
        if not request.is_json:
            return jsonify({'errors': ['Request should be JSON']}), 400

        if id not in bam.menus:
            return jsonify({'errors': ['Not Found']}), 404

        fails, errors = bam.validate_menu_fails(request.json)
        if fails:
            return jsonify({'errors': errors}), 400
        bam.put_menu(request.json, id)
        return jsonify({'message': 'Successfully updated'}), 200


@api.route('/api/v1/menus/<int:id>', methods=['GET'])
def menu(id):
    if id not in bam.menus.keys():
        return jsonify({'errors': ['Not Found']}), 404
    return jsonify(bam.get_menu(id)), 200


"""
Orders Routes

"""


@api.route('/api/v1/orders', methods=['POST', 'GET'])
@jwt_required
def orders():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({
                'errors': ['Request should be JSON']}), 400

        fails, errors = bam.validate_order_fails(request.json)
        if fails:
            return jsonify({'errors': errors}), 400
        return jsonify(bam.post_order(request.json)), 201

    elif request.method == 'GET':
        if not is_caterer():
            return jsonify({
                'errors': ['Unauthorized access to non-caterer']}), 401

        return jsonify({'num_results': len(bam.orders),
                        'objects': list(bam.get_orders().values())})


@api.route('/api/v1/orders/<int:id>', methods=['PATCH', 'GET', 'DELETE'])
@jwt_required
def order(id):
    if request.method == 'GET':
        if not is_caterer():
            return jsonify({
                'errors': ['Unauthorized access to non-caterer']}), 401
        if id not in bam.orders.keys():
            return jsonify({'errors': ['Not Found']}), 404
        return jsonify(bam.get_order(id)), 200

    elif request.method == 'DELETE':
        if id not in bam.orders.keys():
            return jsonify({'errors': ['Not Found']}), 404
        bam.delete_order(id)
        return jsonify({'message': 'Successfully deleted'}), 204

    elif request.method == 'PATCH':
        if not request.is_json:
            return jsonify({'errors': ['Request should be JSON']}), 400

        if id not in bam.orders:
            return jsonify({'errors': ['Not Found']}), 404

        fails, errors = bam.validate_order_fails(request.json)
        if fails:
            return jsonify({'errors': errors}), 400
        bam.put_order(request.json, id)
        return jsonify({'message': 'Successfully updated'}), 200


"""
Notifications Routes

"""


@api.route('/api/v1/notifications', methods=['POST', 'GET'])
@jwt_required
def notifications():
    if not is_caterer():
        return jsonify({
            'errors': ['Unauthorized access to non-caterer']}), 401

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({
                'errors': ['Request should be JSON']}), 400

        fails, errors = bam.validate_notification_fails(request.json)
        if fails:
            return jsonify({'errors': errors}), 400
        return jsonify(bam.post_notification(request.json)), 201

    elif request.method == 'GET':
        return jsonify({'num_results': len(bam.notifications),
                        'objects': list(bam.get_notifications().values())})


@api.route('/api/v1/notifications/<int:id>',
           methods=['PATCH', 'GET', 'DELETE'])
@jwt_required
def notification(id):
    if request.method == 'GET':
        if id not in bam.notifications.keys():
            return jsonify({'errors': ['Not Found']}), 404
        return jsonify(bam.get_notification(id)), 200

    elif request.method == 'DELETE':
        if id not in bam.notifications.keys():
            return jsonify({'errors': ['Not Found']}), 404
        bam.delete_notification(id)
        return jsonify({'message': 'Successfully deleted'}), 204

    elif request.method == 'PATCH':
        if not is_caterer():
            return jsonify({
                'errors': ['Unauthorized access to non-caterer']}), 401

        if not request.is_json:
            return jsonify({'errors': ['Request should be JSON']}), 400

        if id not in bam.notifications:
            return jsonify({'errors': ['Not Found']}), 404

        fails, errors = bam.validate_notification_fails(request.json)
        if fails:
            return jsonify({'errors': errors}), 400
        bam.put_notification(request.json, id)
        return jsonify({'message': 'Successfully updated'}), 200

@api.route('/*')
def not_found():
    return jsonify({'errors': ['Not Found']}), 404
