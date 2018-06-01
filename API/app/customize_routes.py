import json
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask import abort, make_response, jsonify
from app.models import Blacklist, User


def single_for_user(model):
    """
    This returns a flask-restless preprocessor that ensures that this
    user is accessing their own resource if they are not an administrator.

    The preprocessor would return an unauthorized warning if it is not the
    case.

    This assumes that the this user is not a guest.
    """
    def get_single_for_user(instance_id=None, **kwargs):
        """
        Get the logged in user and ensure they are accessing their
        own resource data.
        """
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        if not current_user.is_caterer():
            model_instance = model.query.get(instance_id)
            if current_user.id != model_instance.user_id:
                abort(make_response(
                    jsonify({'message': 'Unauthorized access'}), 
                            401))
    return get_single_for_user


def many_for_user(search_params=None, **kwargs):
    """
    This will change request to ensure the user only accesses their own 
    resource list.

    This assumes the model has a user_id referencing the user and that
    the this user is not a guest.
    """
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    if not current_user.is_caterer():
        search_params['filters'] = [{
            'name': 'user_id', 
            'op': 'eq', 
            'val': current_user.id
        }]


def todays(search_params=None, **kwargs):
    """
    This will ensure the endpoint /menu/ only returns today's menu.

    This assumes the model has a day column.
    """
    search_params['filters'] = [{
        'name': 'day',
        'op': 'eq',
        'val': str(datetime.utcnow().date())
    }] 


def post_delete(was_deleted=None, **kwargs):
    """
    This allows us to add a message to a delete query.
    """
    if was_deleted:
        abort(jsonify({'message': 'Successfully deleted'}))
    else:
        abort(make_response(jsonify({'message': 'Not found'}), 404))


def check_exists(model):
    """
    This allows us to return a custom message if a resource is not 
    found
    """
    def pre_get_model(instance_id=None, **kwargs):
        try: 
            int(instance_id)
        except:
            abort(make_response(jsonify({'message': 'Id must be an integer'}), 
                                400))
        if not model.query.get(instance_id):
            abort(make_response(jsonify({'message': 'Not found'}), 
                                404))
    return pre_get_model

