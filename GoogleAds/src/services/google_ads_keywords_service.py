#import pandas as pd
from utils.generate_mock_metrics import generate_mock_metrics
from services.google_ads_service import get_GoogleAdsClient, get_managed_accounts

def get_keywords_metrics(client, customer_id):
    """Fetches aggregated campaign metrics for a specific client account."""
    query = """
        SELECT
            campaign.id,
            campaign.name,
            ad_group_criterion.criterion_id,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.average_cpc,
            metrics.conversions,
            metrics.cost_per_conversion
        FROM keyword_view
    """
    response = client.get_service("GoogleAdsService").search(customer_id=customer_id, query=query)
    if not response:
        print("No response")

    keyword_match_type_enum = client.get_type("KeywordMatchTypeEnum").KeywordMatchType
    print("\nKeyword Analysis Results:")
    print("=" * 60)
    has_data = False  # Flag to check if any data exists
    keyword_data = []

    for row in response:
        has_data = True  # If at least one row is found, we mark it
        campaign = row.campaign
        keyword = row.ad_group_criterion.keyword.text
        criterion = row.ad_group_criterion
        match_type = keyword_match_type_enum(criterion.keyword.match_type).name
        impressions = row.metrics.impressions or 0
        clicks = row.metrics.clicks or 0
        ctr = row.metrics.ctr or 0
        avg_cpc = row.metrics.average_cpc or 0
        conversions = row.metrics.conversions or 0
        cost_per_conversion = row.metrics.cost_per_conversion or 0

        # add mock data for test accounts         
        mock_metrics = generate_mock_metrics()

        impressions = mock_metrics["Impressions"]
        clicks = mock_metrics["Clicks"]
        conversions = mock_metrics["Conversions"]
        ctr = round((mock_metrics["CTR (%)"] * 100), 1)
        cost_per_conversion = mock_metrics["Conversion Rate (%)"]
        avg_cpc = mock_metrics["Avg CPC (USD)"]
        # end mock data  

        # Append data to the list
        keyword_data.append({
            "CampaignName": campaign.name,
            "CampaignID": campaign.id,
            "Keyword": keyword,
            "MatchType": match_type,
            "Impressions": impressions,
            "Clicks": clicks,
            "Ctr": ctr,
            "AvgCPC": avg_cpc,
            "Conversions": conversions,
            "CostPerConversion": cost_per_conversion
        })

    if not has_data:
        print("⚠️ No keyword data found. Check campaign settings and filters.")
        print("=" * 60)

    return keyword_data

def fetch_keywords_overview():
    """Fetches all keywords metrics for all client accounts under a manager account."""
    client = get_GoogleAdsClient()
    manager_id = client.login_customer_id
    # Step 1: Get all client accounts under the manager account
    client_accounts = get_managed_accounts(client, manager_id)
    print("fetch_manager_overview - client_accounts")
    # Extract list of customer IDs from client_accounts
    customer_ids = [account["customer_id"] for account in client_accounts]
    
    # Step 2: Aggregate performance metrics for all client accounts
    """
    keywords_metrics = {
        "Campaign Name": "",
        "Campaign ID": "",
        "Keyword" : "",
        "Match Type": "",
        "Impressions": 0,
        "Clicks": 0,
        "CTR": 0,
        "Avg CPC": 0,
        "Conversions": 0,
        "Cost/Conversion": 0
    }"
    """
    keywords_metrics = []

    for account_id in customer_ids:
        print("📊 Fetching keywords metrics for client account:")
        account_id_keywords_data = get_keywords_metrics(client, str(account_id))
        print("account_id_keywords_data 1")

        if account_id_keywords_data:
            keywords_metrics.extend(account_id_keywords_data)

        print("keywords_metrics 1")
       
    return keywords_metrics