import requests
from bs4 import BeautifulSoup
import pandas as pd

category = "national" # choose from: national, business, politics, sports, technology, startup, entertainment, hatke, world, automobile, science, travel, miscellaneous, fashion, education, Health___Fitness
url = f"https://inshorts.com/en/read/{category}" # for inshorts

r=requests.get(url)

soup = BeautifulSoup(r.text,"lxml")

# parent_div = soup.find_all("div", {"style":"min-height: calc(-348px + 100vh);"})
# parent_div = soup.find_all("div")

# print(parent_div[0].prettify())

# div = parent_div[0]

# divs_with_class = div.find_all("div", class_="TfxplVx3RtbilOD2tqd6")

# Find the container div
container_div = soup.find("div", id="container")

if container_div:
    # Traverse down the tree to find the div with the class "PmX01nT74iM8UNAIENsC"
    target_div = container_div.find("div", class_="PmX01nT74iM8UNAIENsC")
    
    if target_div:
        print("Found the target div:")
        print(target_div.prettify())
    else:
        print("No div with class 'PmX01nT74iM8UNAIENsC' found.")
else:
    print("Container div not found.")

# print(div.prettify() for div in parent_div)
# for div in parent_div:
#     print(div.prettify())
#     print("---------------------")

# if parent_div:
#     divs_with_class = parent_div.find_all("div", class_="TfxplVx3RtbilOD2tqd6")
#     print(divs_with_class)