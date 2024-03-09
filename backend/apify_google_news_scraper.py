from apify_client import ApifyClient
from dotenv import load_dotenv
# Initialize the ApifyClient with your Apify API token
import os
import json

load_dotenv()
APIFY_API_KEY = os.getenv("APIFY_API_KEY")

client = ApifyClient(APIFY_API_KEY)

# Prepare the Actor input
run_input = {
    "query": "Tesla",
    "language": "IN:en", # "US:en" for news in USA context and similarly for other countries
    "proxyConfiguration": { "useApifyProxy": True },
}

# Run the Actor and wait for it to finish
run = client.actor("lhotanova/google-news-scraper").call(run_input=run_input)

items = [item for item in client.dataset(run["defaultDatasetId"]).iterate_items()]

# Write the items to a JSON file
with open("google_news.json", "w") as json_file:
    json.dump(items, json_file, indent=4)

# # Fetch and print Actor results from the run's dataset (if there are any)
# for item in client.dataset(run["defaultDatasetId"]).iterate_items():
#     print(item)
