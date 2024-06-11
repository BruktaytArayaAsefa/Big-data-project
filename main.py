from src.downloader import download_volumes
from src.extractor import extract_data_from_pdfs
from database import connect_elasticsearch, create_index, index_all_json_files  # Import necessary functions

ceur_ws_url = "https://ceur-ws.org"
ceur_ws_downloads_dir = "ceur_ws_downloads"
output_dir = "output"
index_name = 'conference_papers'  # Define your index name

# Download volumes
download_volumes(ceur_ws_url, ceur_ws_downloads_dir)

# Extract data from PDF files
extract_data_from_pdfs(ceur_ws_downloads_dir, output_dir)

# Connect to Elasticsearch and create the index
es = connect_elasticsearch()
create_index(es, index_name)

# Index the extracted data to Elasticsearch
index_all_json_files(es, index_name, output_dir)
