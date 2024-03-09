from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

params = {
  "engine": "google",
  "q": "Coffee",
  "api_key":SERP_API_KEY
}

search = GoogleSearch(params)
results = search.get_dict()
# organic_results = results["organic_results"]
print(results)