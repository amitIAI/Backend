import random 

def generate_mock_metrics():
    """Generates random mock performance metrics for ads."""
    return {
        "Impressions": random.randint(100, 50000),
        "Clicks": random.randint(5, 5000),
        "CTR (%)": round(random.uniform(0.005, 0.1), 3),
        "Conversions": random.randint(0, 200),
        "Cost (USD)": random.randint(500, 20000),
        "Conversion Rate (%)": round(random.uniform(1, 20), 2),
        "View Rate (%)": round(random.uniform(5, 30), 2),
        "Avg CPC (USD)": round(random.uniform(0.3, 5.0), 2),
    }