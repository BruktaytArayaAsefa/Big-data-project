import os
import requests

def download_volumes(ceur_ws_url, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Check if zip files already exist in output directory
    existing_zips = set(os.listdir(output_dir))
    
    # Download volumes only if they don't exist
    for i in range(1, 3674):  
        volume_zip = f"Vol-{i}.zip"
        if volume_zip not in existing_zips:
            volume_url = f"{ceur_ws_url}/{volume_zip}"
            response = requests.get(volume_url)
            with open(os.path.join(output_dir, volume_zip), "wb") as f:
                f.write(response.content)