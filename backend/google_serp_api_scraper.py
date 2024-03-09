from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
import json

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

params = {
  "q": "stock market", # search query
  "location": "India", # country searching in
  "hl": "en", # language
  "gl": "in", # geolocation
  "google_domain": "google.com",
  "tbm": "nws", # search type
  "num": "20", # no. of results
  "start": "0", # at which result to start
  "safe": "active", # adult content filter
  "api_key": SERP_API_KEY
}

search = GoogleSearch(params)
results = search.get_dict()

with open("google_serp_api.json", "w") as json_file:
    json.dump(results["news_results"], json_file, indent=4)
    
# print(json.dumps(results, indent=2))