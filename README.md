<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<br />

<!-- PROJECT LOGO -->
<div align="center">
  <img src="image/big-data-logo.png" alt="Logo" width="450" height="250">
  <h3 align="center">CEUR-WS Data Downloader and Indexer</h3>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project
This project is designed to download volumes from the CEUR-WS website, extract data from the zip files, and index this data into an Elasticsearch database for easy searching and analysis.The data is extracted from PDF files and HTML metadata within each zip file, saved as JSON files, and indexed in Elasticsearch.

### Built With
* ![Python](https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white)
* ![Elasticsearch](https://img.shields.io/badge/elasticsearch-%23005571.svg?style=for-the-badge&logo=elasticsearch&logoColor=white)
* ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites
* **Python** and **pip**
* **Docker** (for Elasticsearch)
* **Elasticsearch** running locally or in a Docker container
<strong>Elasticsearch Database</strong> and <strong>DOCKER</strong>

Below are the steps to run Elasticsearch using docker. If you want to run Elasticsearch without docker you can refer to the instructions <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#:~:text=Start%20a%20single-node%20cluster%20edit%201%20Install%20Docker.,Elasticsearch%20to%20ensure%20the%20Elasticsearch%20container%20is%20running.">here</a>.
Please follow the steps in installation to create and run the Elasticsearch docker container.
### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your_username/your_repo.git
<strong>Elasticsearch Database</strong>

##### Using Docker

1. Ensure Docker is installed and running on your machine. If not, follow the instructions [here](https://docs.docker.com/get-docker/).

2. For the first time, ensure that you configure Elasticsearch properly in the `docker-compose.yml` file.

    ```yaml
    elasticsearch:
        image: docker.elastic.co/elasticsearch/elasticsearch:7.10.1
        container_name: elasticsearch
        environment:
          - discovery.type=single-node
        ports:
          - 9200:9200
        volumes:
          - es_data:/usr/share/elasticsearch/data
    ```

3. Run the following command to start the Elasticsearch service:

    ```sh
    docker compose up -d
    ```

    Note: If you encounter a `docker compose command not found` error, use a dash between `docker` and `compose` as shown below:

    ```sh
    docker-compose up -d
    ```

4. Verify Elasticsearch is running by accessing the interface at [http://localhost:9200](http://localhost:9200).

5. If you need to stop the Docker container, use the following command:

    ```sh
    docker compose down
    ```

 ##### Without Docker

1. Download and install Elasticsearch from the official website [here](https://www.elastic.co/downloads/elasticsearch).

2. Extract the downloaded file and navigate to the Elasticsearch directory.

3. Start Elasticsearch by running the following command:

    **Windows:**

    ```sh
    bin\elasticsearch.bat
    ```

    **MacOS/Linux:**

    ```sh
    bin/elasticsearch
    ```

4. Verify Elasticsearch is running by accessing the interface at [http://localhost:9200](http://localhost:9200).

<br />



5. Install Python dependencies:
    ```sh
    pip install -r requirements.txt



6. Start Elasticsearch using Docker:
   ```sh
    docker run -d -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.10.1

<br />
 
### Usage

<details>
  <summary>Download Volumes</summary>
  <p>Run the following command to download volumes from the CEUR-WS website:</p>
  
  <pre><code>python downloader.py</code></pre>
</details>

<details>
  <summary>Extract Data</summary>
  <p>Run the following command to extract data from the downloaded PDF files:</p>
  
  <pre><code>python extractor.py</code></pre>
</details>

<details>
  <summary>Index Data to Elasticsearch</summary>
  <p>Make sure Elasticsearch is running, then run the following command to index data:</p>
  
  <pre><code>python database.py</code></pre>
</details>

<details>
  <summary>Combining All Steps</summary>
  <p>You can also run all steps sequentially using <code>main.py</code>:</p>
  
  <pre><code>python main.py</code></pre>
</details>