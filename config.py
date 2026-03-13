from dotenv import dotenv_values

config = dotenv_values(".env")

BLOB_CONNECTION_STRING = config["BLOB_CONNECTION_STRING"]
CONTAINER_NAME = config["CONTAINER_NAME"]

FOUNDRY_ENDPOINT = config["FOUNDRY_ENDPOINT"]
TENANT_ID = config["TENANT_ID"]
MODEL_NAME = config["MODEL_NAME"]