import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from time import sleep
from azure.cosmos import CosmosClient, PartitionKey
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

sitemap_url = "https://www.etown.edu/sitemap.xml"
response = requests.get(sitemap_url)
sitemap_xml = response.content

root = ET.fromstring(sitemap_xml)
urls = [url.text for url in root.findall(
    './/{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]

endpoint = "https://hoya24.documents.azure.com:443/"
key = os.getenv("AZURE_COSMOS_DB_KEY")
client = CosmosClient(endpoint, key)

database_id = "hoya24"
container_id = "sitetext"

database = client.create_database_if_not_exists(id=database_id)
container = database.create_container_if_not_exists(
    id=container_id,
    partition_key=PartitionKey(path="/url")
)

for url in urls:
    sleep(5)

    try:
        page_response = requests.get(url)

        if page_response.status_code == 200:
            soup = BeautifulSoup(page_response.content, 'html.parser')

            # Look for a meta tag that indicates a 404 or similar error
            meta_tag = soup.find(
                'meta', attrs={'name': 'description', 'content': '404 error'})

            # If such a meta tag is found, consider it as an error page
            if meta_tag:
                print(f"Page not found (via meta tag): {url}")
                continue

            main_content = soup.find(id="main-content")

            if main_content:
                text = ' '.join(main_content.stripped_strings)
            else:
                print(f"No main content found for URL: {url}")
                text = ' '.join(soup.stripped_strings)

            query = "SELECT c.id FROM c WHERE c.url = @url"
            result = list(container.query_items(
                query=query, parameters=[{"name": "@url", "value": url}], enable_cross_partition_query=True))

            existingId = result[0]['id'] if len(result) > 0 else None

            if existingId:
                data = {
                    "id": existingId,
                    "url": url,
                    "text": text,
                }
                container.upsert_item(body=data)
            else:
                data = {
                    "id": str(uuid.uuid4()),
                    "url": url,
                    "text": text,
                }
                container.create_item(body=data)
        else:
            print(f"HTTP Error: {page_response.status_code} for URL: {url}")
    except Exception as e:
        print(e)
