from google.ads.googleads.client import GoogleAdsClient
from config.config import Config

# Load Google Ads Client
client = GoogleAdsClient.load_from_storage(Config.GOOGLE_ADS_YAML_PATH, version="v19")

def get_managed_accounts(manager_customer_id):
    """Fetches all customer accounts managed by an MCC (manager account)."""
    query = """
        SELECT customer_client.id, customer_client.descriptive_name
        FROM customer_client
        WHERE customer_client.manager = FALSE
    """
    response = client.get_service("GoogleAdsService").search(
        customer_id=str(manager_customer_id), query=query
    )
    
    accounts = []
    for row in response:
        accounts.append({
            "customer_id": row.customer_client.id,
            "name": row.customer_client.descriptive_name
        })
    return accounts

def get_campaigns(customer_id):
    """Fetches all campaigns under a given customer account."""
    query = """
        SELECT campaign.id, campaign.name, campaign.status
        FROM campaign
        ORDER BY campaign.id
    """
    response = client.get_service("GoogleAdsService").search(
        customer_id=str(customer_id), query=query
    )
    
    campaigns = []
    for row in response:
        campaigns.append({
            "campaign_id": row.campaign.id,
            "name": row.campaign.name,
            "status": row.campaign.status.name
        })
    return campaigns