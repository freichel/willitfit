"""
Module for interaction with Google Cloud Storage
"""

from google.cloud import storage
from numpy.lib import index_tricks
from willitfit.params import (
    BUCKET_NAME,
    DATA_FOLDER,
    CAR_DATABASE,
    GOOGLE_APPLICATION_CREDENTIALS,
    PROJECT_DIR,
    PROJECT_NAME,
)
import pandas as pd
import os


def get_cloud_data(path_to_file=f"{DATA_FOLDER}/{CAR_DATABASE}"):
    """
    Returns data from chosen path as dataframe.
    """
    # Set environment variable for service account
    set_environment_variable()

    # Read and return data
    return pd.read_csv(f"gs://{BUCKET_NAME}/{path_to_file}")


def send_cloud_data(df, path_to_file="data/test.csv"):
    """
    Saves a dataframe to a local copy of a file, then pushes it to specified path.
    Returns True once upload complete.
    """
    # Set environment variable for service account
    set_environment_variable()

    # Initiate client
    storage_client = storage.Client()

    # Specify bucket
    bucket = storage_client.bucket(BUCKET_NAME)

    # Write dataframe

    df.to_csv(PROJECT_DIR / PROJECT_NAME / path_to_file, index=False)

    # Create blob
    blob = bucket.blob(path_to_file)

    # Upload blob
    blob.upload_from_filename(PROJECT_DIR / PROJECT_NAME / path_to_file)

    return True


def set_environment_variable():
    # Set environment variable for service account
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        str(PROJECT_DIR) + "/" + GOOGLE_APPLICATION_CREDENTIALS
    )
