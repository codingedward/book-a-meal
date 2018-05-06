from flask import abort, make_response, jsonify


def post_delete(was_deleted=None, **kwargs):
    if was_deleted:
        abort(jsonify({'message': 'Successfully deleted'}))
    else:
        abort(make_response(jsonify({'message': 'Not found'}), 404))

def post_get(result=None, **kwargs):
    print(result) 
    print(kwargs)
    if not result or len(result) == 0:
        abort(make_response(jsonify({'message': 'Not found'}), 400))

