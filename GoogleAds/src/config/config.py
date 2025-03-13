import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='./config/.env')

GOOGLE_ADS_YAML_PATH = os.getenv("GOOGLE_ADS_YAML_PATH")
#print("GOOGLE_ADS_YAML_PATH is:", GOOGLE_ADS_YAML_PATH)

class Config:
    GOOGLE_ADS_YAML_PATH = os.getenv("GOOGLE_ADS_YAML_PATH")
    CUSTOMER_ID = os.getenv("account_id")
    CUSTOMER_ID_LIST = os.getenv("account_id_list")

'''
class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
'''