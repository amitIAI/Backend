import os
from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient
from utils.generate_mock_metrics import generate_mock_metrics

# Load Google Ads Client, if no path load from home directory
# client = GoogleAdsClient.load_from_storage(Config.GOOGLE_ADS_YAML_PATH, version="v19")
def get_GoogleAdsClient():
    print("get_GoogleAdsClient")

    #    Replace in production
    #########################################
    load_dotenv(dotenv_path='./.env')

    DEVELOPER_TOKEN = os.getenv("DEVELOPER_TOKEN")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
    MCC_ID = os.getenv("MCC_ID")
    
    config ={
        "developer_token": DEVELOPER_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "login_customer_id": MCC_ID,
        "use_proto_plus" : True,
    
    }
    #client = GoogleAdsClient.load_from_storage(version="v19")
    ################################################################

    client = GoogleAdsClient.load_from_dict(config, version="v19")
    
    print("YES CLIENT")
    return (client)


def get_managed_accounts(client, manager_customer_id):
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

def get_campaigns(client, customer_id):
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

def get_aggregated_metrics(client, customer_id):
    """Fetches aggregated campaign metrics for a specific client account."""
    query = """
        SELECT
            metrics.impressions,
            metrics.average_cpm,
            metrics.clicks,
            metrics.ctr,
            metrics.cost_micros,
            metrics.conversions,
            metrics.cost_per_conversion,
            metrics.average_cpc
        FROM customer
    """
    response = client.get_service("GoogleAdsService").search(customer_id=customer_id, query=query)
    if not response:
        print("No response")

    # Initialize totals
    total_impressions = total_clicks = total_cost_micros = total_conversions = 0
    total_ctr = total_cpm_micros = total_cost_per_conversion_micros = total_avg_cpc_micros = 0
    count = 0  # Used for averaging CPM & CPC

    for row in response:
        """
        uncomment for live data
        total_impressions += row.metrics.impressions or 0
        total_clicks += row.metrics.clicks or 0
        total_cost_micros += row.metrics.cost_micros or 0
        total_conversions += row.metrics.conversions or 0
        total_ctr += row.metrics.ctr or 0
        total_cpm_micros += row.metrics.average_cpm or 0
        total_cost_per_conversion_micros += row.metrics.cost_per_conversion or 0
        total_avg_cpc_micros += row.metrics.average_cpc or 0
        count += 1
        """

        # add mock data for test accounts         
        mock_metrics = generate_mock_metrics()

        total_impressions += mock_metrics["Impressions"]
        total_clicks += mock_metrics["Clicks"]
        total_cost_micros += mock_metrics["Cost (USD)"]
        total_conversions += mock_metrics["Conversions"]
        total_ctr += mock_metrics["CTR (%)"]
        total_cpm_micros += mock_metrics["View Rate (%)"]
        total_cost_per_conversion_micros += mock_metrics["Conversion Rate (%)"]
        total_avg_cpc_micros += mock_metrics["Avg CPC (USD)"]
        count += 1
        # end mock data  


    # Prevent division by zero
    avg_cpm = (total_cpm_micros / count) if count else 0
    avg_ctr = (total_ctr / count) * 100 if count else 0
    avg_cpc = (total_avg_cpc_micros / count) if count else 0
    cost_per_conversion = (total_cost_per_conversion_micros / count) / 1_000_000 if count else 0

    return {
        "Total Impressions": total_impressions,
        "CPM (USD)": avg_cpm,
        "Total Clicks": total_clicks,
        "CTR (%)": round(avg_ctr, 2),
        "Total Cost (USD)": total_cost_micros,
        "Total Conversions": total_conversions,
        "Cost/Conversion (USD)": cost_per_conversion,
        "Avg CPC (USD)": round(avg_cpc,2)
    }

def fetch_manager_overview():
    """Fetches aggregated performance metrics for all client accounts under a manager account."""
    # Step 1: Get all client accounts under the manager account
    client = get_GoogleAdsClient()
    manager_id = client.login_customer_id
    client_accounts = get_managed_accounts(client, manager_id)
    print("fetch_manager_overview - client_accounts")
    # Extract list of customer IDs
    customer_ids = [account["customer_id"] for account in client_accounts]
    
    # Step 2: Aggregate performance metrics for all client accounts
    aggregated_data = {
        "Total Impressions": 0,
        "CPM (USD)": 0,
        "Total Clicks": 0,
        "CTR (%)": 0,
        "Total Cost (USD)": 0,
        "Total Conversions": 0,
        "Cost/Conversion (USD)": 0,
        "Avg CPC (USD)": 0
    }
    account_count = 0

    for account_id in customer_ids:
        print("📊 Fetching metrics for client account")
        account_metrics = get_aggregated_metrics(client, str(account_id))
        print("aggregated_data 1")
        # Sum total metrics
        aggregated_data["Total Impressions"] += account_metrics["Total Impressions"]
        aggregated_data["Total Clicks"] += account_metrics["Total Clicks"]
        aggregated_data["Total Cost (USD)"] += account_metrics["Total Cost (USD)"]
        aggregated_data["Total Conversions"] += account_metrics["Total Conversions"]
        print("aggregated_data 2")

        # Running total for averaging CPM, CTR, CPC
        aggregated_data["CPM (USD)"] += account_metrics["CPM (USD)"]
        aggregated_data["CTR (%)"] += account_metrics["CTR (%)"]
        aggregated_data["Cost/Conversion (USD)"] += account_metrics["Cost/Conversion (USD)"]
        aggregated_data["Avg CPC (USD)"] += account_metrics["Avg CPC (USD)"]

        account_count += 1
        print("aggregated_data 3; account_count =")
    # Compute average values
    if account_count > 0:
        aggregated_data["CPM (USD)"] = round(aggregated_data["CPM (USD)"] / account_count, 2)
        aggregated_data["CTR (%)"] = round(aggregated_data["CTR (%)"] / account_count, 2)
        aggregated_data["Cost/Conversion (USD)"] = round(aggregated_data["Cost/Conversion (USD)"] / account_count, 2)
        aggregated_data["Avg CPC (USD)"] = round(aggregated_data["Avg CPC (USD)"] / account_count, 2)
        print("aggregated_data 4" )
    return aggregated_data