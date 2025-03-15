from flask import Blueprint, jsonify, request
from services.google_ads_service import get_GoogleAdsClient, get_managed_accounts, get_campaigns

campaign_bp = Blueprint('campaigns', __name__)

@campaign_bp.route('/campaigns', methods=['GET'])
def campaigns():
    """API endpoint to fetch all campaigns under all managed accounts."""
    """manager_id = request.args.get("manager_id")
    if not manager_id:
        return jsonify({"error": "Missing manager_id parameter"}), 400"""

    try:
        client = get_GoogleAdsClient()
        manager_id = client.login_customer_id
        accounts = get_managed_accounts(client, manager_id)
        all_campaigns = {}

        for account in accounts:
            all_campaigns[account["customer_id"]] = get_campaigns(client, account["customer_id"])

        return jsonify(all_campaigns)

    except Exception as e:
        return jsonify({"error": str(e)}), 500