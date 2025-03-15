"""

from flask import Blueprint, request, jsonify
from services.user_service import get_user_by_id, create_user

user_bp = Blueprint('users', __name__)

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({'message': 'User not found'}), 404

@user_bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    user = create_user(data)
    return jsonify(user), 201

"""