import requests
import pandas as pd
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from dotenv import dotenv_values

# ---------------------------------
# Load configuration
# ---------------------------------

config = dotenv_values(".env")

BLOB_CONNECTION_STRING = config["BLOB_CONNECTION_STRING"]
CONTAINER_NAME = config["CONTAINER_NAME"]

# ---------------------------------
# Connect to Azure Blob
# ---------------------------------

blob_service_client = BlobServiceClient.from_connection_string(
    BLOB_CONNECTION_STRING
)

container_client = blob_service_client.get_container_client(CONTAINER_NAME)

try:
    container_client.create_container()
except:
    pass


# ---------------------------------
# Helper function: fetch API data
# ---------------------------------

def fetch_data(endpoint):

    url = f"https://api.openf1.org/v1/{endpoint}?session_key=latest"

    response = requests.get(url)

    if response.status_code != 200:
        print("API error:", response.status_code)
        return None

    data = response.json()

    if isinstance(data, list) and len(data) > 0:
        return pd.DataFrame(data)
    else:
        print(f"No data returned for {endpoint}")
        return None


# ---------------------------------
# Upload dataframe to blob
# ---------------------------------

def upload_dataframe(df, name):

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    file_name = f"{name}_{timestamp}.csv"

    df.to_csv(file_name, index=False)

    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME,
        blob=file_name
    )

    with open(file_name, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    print(f"Uploaded {file_name}")


# ---------------------------------
# Fetch datasets
# ---------------------------------

print("Fetching latest F1 session data...")

drivers_df = fetch_data("drivers")
laps_df = fetch_data("laps")
results_df = fetch_data("session_result")


# ---------------------------------
# Upload to Blob
# ---------------------------------

if drivers_df is not None:
    upload_dataframe(drivers_df, "drivers")

if laps_df is not None:
    upload_dataframe(laps_df, "laps")

if results_df is not None:
    upload_dataframe(results_df, "race_results")


print("Extraction completed.")