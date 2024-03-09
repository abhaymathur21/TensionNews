import json
import requests
from bs4 import BeautifulSoup

# DESCRIPTION AND TAGS EXTRACTION FROM METADATA OF WEBSITES IN DATABASE    
    
# with open('backend/google_serp_api.json', 'r') as file:
#     data = json.load(file)    
    
article_links = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
  }

def extract_metadata(article_links):
        
    article_description = []
    article_keywords = []
    article_title = []
    
    for link in article_links:
        response_ = requests.get(link, headers=headers)
        soup_ = BeautifulSoup(response_.content, "lxml")
        title = soup_.find("title")
        article_title.append(title.text)
        desc_meta_tag = soup_.find('meta', attrs={'name': 'description'})
        if desc_meta_tag:
            description = desc_meta_tag.get('content')
            article_description.append(description)
            
        keywords_meta_tag = soup_.find('meta', attrs={'name': 'keywords'})
        if keywords_meta_tag:
            keywords = keywords_meta_tag.get('content')
            article_keywords.append(keywords)
            
    return article_description, article_keywords, article_title