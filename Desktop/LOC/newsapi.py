import json
from dateutil.relativedelta import relativedelta
import datetime
import requests
import os
from dotenv import load_dotenv
load_dotenv()


def get_news(query, api_key):
    url = "https://newsapi.org/v2/everything?q=tesla&from=2024-02-09&sortBy=publishedAt&apiKey=1c71a23cdb2b4d37987282bfe675c96f"
    current_date = datetime.datetime.now()
    past_date = current_date - relativedelta(hours=30)
    current_date_str = current_date.strftime('%Y-%m-%dT%H:%M:%S')
    past_date_str = past_date.strftime('%Y-%m-%dT%H:%M:%S')

    parameters = {
        'q': query,
        'from': past_date_str,
        'to': current_date_str,
        'sortBy': 'popularity',
        'language': 'en',
    }

    response = requests.get(url, params=parameters)
    data = response.json()
    articles = data["articles"][:20]

    return articles


def main():
    query = "Artificial Intelligence"
    api_key = os.getenv("NEWSAPI")
    articles = get_news(query, api_key)

    output = []
    for i, article in enumerate(articles, 1):
        output.append({
            'title': '"'+article['title'] + '"',
            'url': article['url'],
            'source': 'source... '+article['source']['name'],
            'publishedAt': article['publishedAt'],
            'description': '"'+article['description'] + '"',
            'content': '"'+article['content'] + '"',
            'urlToImage': article['urlToImage']
        })
    output.reverse()
    with open('generated_script.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4)


if __name__ == "__main__":
    main()