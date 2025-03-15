from flask import Blueprint, jsonify, request
from services.google_ads_service import fetch_manager_overview

customer_metrics_bp = Blueprint('cust_metrics', __name__)

@customer_metrics_bp.route('/aggregated_metrics', methods=['GET'])
def aggregated_metrics():
    """API endpoint to fetch aggregated overview metrics for all managed accounts."""
    """manager_id = request.args.get("manager_id")
    if not manager_id:
        return jsonify({"error": "Missing manager_id parameter"}), 400"""

    try:
        print("Fetching aggregated metrics for manager_id:customer_metrics_bp")
        aggregated_data = fetch_manager_overview()
        print("Aggregated data:customer_metrics_bp")
        return jsonify(aggregated_data)

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

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