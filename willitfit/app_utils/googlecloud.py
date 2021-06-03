'''
Module for interaction with Google Cloud Storage
'''

from google.cloud import storage
from dotenv import load_dotenv
from willitfit.params import PROJECT_DIR, ENV_FILE


def get_cloud_data():
    # Load key
    load_dotenv(dotenv_path=PROJECT_DIR/ENV_FILE)
    
    # Initiate client
    storage_client = storage.Client()
    
    # 
    bucket = 
    
if __name__ == "__main__":
    print(get_cloud_data())