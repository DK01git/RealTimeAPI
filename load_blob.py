import pandas as pd
from azure.storage.blob import BlobServiceClient
from io import BytesIO
from config import BLOB_CONNECTION_STRING, CONTAINER_NAME


def load_latest_pq():

    blob_service = BlobServiceClient.from_connection_string(
        BLOB_CONNECTION_STRING
    )

    container_client = blob_service.get_container_client(CONTAINER_NAME)

    blobs = list(container_client.list_blobs())

    if len(blobs) == 0:
        raise Exception("No files found")

    latest_blob = sorted(blobs, key=lambda x: x.last_modified)[-1]

    blob_client = container_client.get_blob_client(latest_blob.name)

    stream = BytesIO()
    blob_client.download_blob().readinto(stream)
    stream.seek(0)
    df = pd.read_parquet(stream)

    print("Loaded:", latest_blob.name)

    return df