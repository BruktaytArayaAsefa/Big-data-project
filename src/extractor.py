import os
import json
from PyPDF2 import PdfReader
from zipfile import ZipFile
import re
import shutil
import warnings
from bs4 import BeautifulSoup
from base64 import b64encode
from .keyword_extractor import extract_keywords_from_abstract  # Import the keyword extraction function
from database import connect_elasticsearch, index_data  # Import Elasticsearch functions

def extract_data_from_pdfs(zip_dir, output_dir):
    es = connect_elasticsearch()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for zip_file in os.listdir(zip_dir):
        if zip_file.endswith(".zip"):
            zip_path = os.path.join(zip_dir, zip_file)
            try:
                data, json_file_path = extract_data_from_zip(zip_path, output_dir)  # Extract data and get JSON file path
                index_data(es, "conference_papers", data)  # Index data directly to Elasticsearch
                print(f"Saved JSON file: {json_file_path}")  # Print path of saved JSON file
            except Exception as e:
                print(f"Failed to process {zip_file}: {e}")

def extract_data_from_zip(zip_path, output_dir):
    extracted_data = []
    extract_dir = os.path.splitext(zip_path)[0]
    json_file_path = os.path.join(output_dir, os.path.basename(extract_dir) + ".json")  # Path to save JSON file
    
    with ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
        
        html_index_file = None
        for file in zip_ref.namelist():
            if file.endswith(".html"):  # Step 2: Extract HTML index file
                html_index_file = file
                break
        
        if html_index_file:
            html_index_path = os.path.join(extract_dir, html_index_file)
            metadata = extract_metadata_from_html(html_index_path)  # Step 3: Extract metadata from HTML
        else:
            metadata = {"volume_title": "", "conference_name": "", "authors": ""}  # Default metadata if HTML index file not found

        # Extract volume title and conference name once
        authors = metadata.get('authors', '')
        volume_title = metadata.get('volume_title', '')
        conference_name = metadata.get('conference_name', '')

        for pdf_file in zip_ref.namelist():
            if pdf_file.endswith(".pdf"):
                pdf_path = os.path.join(extract_dir, pdf_file)
                try:
                    # Include volume title and conference name in the output data
                    extracted_data.append(extract_data_from_pdf(pdf_path, volume_title, conference_name, authors))
                except Exception as e:
                    print(f"Failed to extract data from {pdf_file}: {e}")
   # Save extracted data as JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(extracted_data, json_file, indent=4)
    
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    
    return extracted_data, json_file_path
def extract_data_from_pdf(pdf_path, volume_title, conference_name, authors):
    try:
        with open(pdf_path, "rb") as f:
            # Suppress all warnings from PyPDF2
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                pdf = PdfReader(f)
                
            # Extract the title and authors
            title = extract_title(pdf)
            abstract = extract_abstract(pdf)
            keywords = extract_keywords(pdf)
            # Extract additional keywords from the abstract using the new module
            nlp_keywords = extract_keywords_from_abstract(abstract)
            
            # Read the PDF content as binary data
            pdf_content = f.read()
            encoded_pdf = b64encode(pdf_content).decode('utf-8')

        return {
            "title": title, "authors": authors, "abstract": abstract, "keywords": keywords, "Keywordfs": nlp_keywords,
            "volume_title": volume_title, "conference_name": conference_name, "pdf_data": encoded_pdf
        }
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return {
            "title": "", "authors": "", "abstract": "", "keywords": [], "Keywordfs": [], 
            "volume_title": volume_title, "conference_name": conference_name, "pdf_data": ""
        }

def extract_title(pdf):
    title = ""
    try:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Try to find title in the first page, usually in the first lines
                lines = text.split('\n')
                for line in lines:
                    # A heuristic: titles are usually in title case and can be quite descriptive
                    if line.strip() and (line.istitle() or len(line.split()) > 3):
                        title = line.strip()
                        return title
    except Exception as e:
        print(f"Error extracting title: {e}")
    return title

def extract_abstract(pdf):
    abstract = ""
    try:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                match = re.search(r'abstract', text, re.IGNORECASE)
                if match:
                    start_index = match.start()
                    # Capture text till the end of the abstract section or some end indicator (e.g., next heading)
                    abstract = text[start_index:].split("\n\n", 1)[0].strip()
                    break
    except Exception as e:
        print(f"Error extracting abstract: {e}")
    return abstract

def extract_keywords(pdf):
    keywords = []
    try:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                match = re.search(r'keywords', text, re.IGNORECASE)
                if match:
                    start_index = match.start()
                    keywords_text = text[start_index:].split("\n\n", 1)[0].strip()
                    # Assuming keywords are comma-separated
                    keywords = [kw.strip() for kw in keywords_text.split(',')]
                    break
    except Exception as e:
        print(f"Error extracting keywords: {e}")
    return keywords

def extract_metadata_from_html(html_path):
    try:
        with open(html_path, "r") as f:
            soup = BeautifulSoup(f, 'html.parser')
            volume_title = soup.title.string.strip() if soup.title else ""
            conference_name = soup.find("h1").text.strip() if soup.find("h1") else ""
            # Assuming authors are listed in a meta tag or a specific class in HTML
            author_meta = soup.find('meta', {'name': 'CEURAUTHORS'})
            if author_meta and 'content' in author_meta.attrs:
                authors = author_meta['content']
            else:
                author_tag = soup.find(class_='CEURAUTHORS')
                authors = author_tag.get_text(strip=True) if author_tag else ""
            return {"volume_title": volume_title, "conference_name": conference_name, "authors": authors}
    except Exception as e:
        print(f"Error parsing HTML {html_path}: {e}")
        return {"volume_title": "", "conference_name": "", "authors": ""}

def save_data_as_json(data, output_file):
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)
