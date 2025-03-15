from flask import Blueprint, jsonify, request
from services.google_ads_keywords_service import fetch_keywords_overview

all_keywords_bp = Blueprint('all_keywords', __name__)

@all_keywords_bp.route('/all_keywords_metrics', methods=['GET'])
def all_keywords_metrics():
    """API endpoint to fetch metrics of all keywords for all managed accounts."""
    """manager_id = request.args.get("manager_id")
    if not manager_id:
        return jsonify({"error": "Missing manager_id parameter"}), 400"""

    try:
        print("Fetching aggregated metrics for manager_id: all_keywords_bp")
        keywords_metrics = fetch_keywords_overview()
        print("keywords_metrics data:all_keywords_bp ")
        return jsonify(keywords_metrics)

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500
