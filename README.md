# F1 Data Extraction Notebook

This notebook automates the process of extracting Formula 1 (F1) race data from the OpenF1 API and uploading it to Azure Blob Storage for further analysis or storage.

## Prerequisites

- Microsoft Fabric environment with access to Azure services
- Azure Key Vault with the following secrets:
  - `storageKey`: Connection string for Azure Blob Storage
  - `container`: Name of the blob container
- Required Python packages: `requests`, `pandas`, `azure-storage-blob`

## Procedure Overview

1. **Install Dependencies**: Install necessary Python packages using pip.
2. **Import Libraries**: Load required libraries for API calls, data manipulation, and Azure Blob Storage interaction.
3. **Retrieve Secrets**: Fetch Azure Blob Storage connection string and container name from Azure Key Vault.
4. **Connect to Blob Storage**: Establish connection to Azure Blob Storage and ensure the container exists.
5. **Fetch F1 Data**: Retrieve the latest F1 session data including drivers, laps, and race results from the OpenF1 API.
6. **Upload Data**: Save the fetched data as CSV files (with .parquet extension in filename) and upload them to the specified Azure Blob container.

## Data Sources

- **OpenF1 API**: Public API providing real-time and historical F1 data (https://api.openf1.org/v1/)

## Output

The notebook generates and uploads the following files to Azure Blob Storage:

- `drivers_[timestamp].parquet` (actually CSV format)
- `laps_[timestamp].parquet` (actually CSV format)
- `race_results_[timestamp].parquet` (actually CSV format)

## Usage

1. Open the notebook in Microsoft Fabric.
2. Ensure the Azure Key Vault secrets are properly configured.
3. Run the cells in order to execute the data extraction and upload process.
4. Check the Azure Blob Storage container for the uploaded files.

## Notes

- The notebook fetches data for the "latest" session key from the OpenF1 API.
- Files are timestamped to avoid overwrites.
- Error handling is minimal; check console output for any API or upload issues.
