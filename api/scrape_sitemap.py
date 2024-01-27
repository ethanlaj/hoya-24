import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from time import sleep
from db import db

sitemap_url = "https://www.etown.edu/sitemap.xml"
response = requests.get(sitemap_url)
sitemap_xml = response.content

root = ET.fromstring(sitemap_xml)
urls = [url.text for url in root.findall(
        './/{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]

site_text = db.sitetext

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

            # Insert or update the text in the database
            site_text.update_one(
                {'url': url}, {'$set': {'text': text}}, upsert=True)
        else:
            print(f"HTTP Error: {page_response.status_code} for URL: {url}")
    except Exception as e:
        print(e)
