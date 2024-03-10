from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from sqlalchemy.dialects.postgresql import JSONB
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from textblob import TextBlob

from llm import llm_response
from metadata import extract_metadata
from stock_analysis.stock_analysis import stock_extraction

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.bmkjkdaiqpvixkkjdlhp:TensionFlowLOC@aws-0-ap-south-1.pooler.supabase.com:5432/postgres'

# Define your models here

class SerpTest(db.Model):
    __tablename__ = 'SerpTest'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    position_in_search = db.Column(db.Integer)
    date_of_news = db.Column(db.String)
    title = db.Column(db.String)
    link_to_article = db.Column(db.String)
    snippet = db.Column(db.String)
    tags = db.Column(JSONB)
    source = db.Column(db.String)
    vectors = db.Column(db.JSON)
    company = db.Column(db.String)
    location = db.Column(db.String)
    closing_price = db.Column(db.JSON)
    volume = db.Column(db.JSON)
    sentiment = db.Column(db.String)
        
db.init_app(app)

# with open('backend/google_serp_api.json', 'r') as file:
#     data = json.load(file)

# article_links = []
# vector_embeddings = []
# embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# for entry in data:
#     article_links.append(entry["link"])

# article_description, article_keywords, article_title = extract_metadata(article_links)

# for article in article_description:
#     vector_embeddings.append(embeddings.embed_query(article))

    
# # TO ADD NEW ENTRIES TO THE DATABASE, UNCOMMENT THE FOLLOWING CODE:  
    
# with app.app_context():
#     db.create_all()        
    
#     for i, entry in enumerate(data, start=0):
                
#         new_entry = SerpTest(position_in_search = entry["position"], date_of_news = entry["date"], title = entry["title"], link_to_article = entry["link"], snippet = article_description[i], tags= article_keywords[i], source = entry["source"], vectors = vector_embeddings[i])
        
#         # Add the new entry to the session
#         db.session.add(new_entry)
        
#         db.session.commit() 
        
#     db.session.close()
    
    
with app.app_context():    
    
    db_data = SerpTest.query.all()
    
    article_links = []
    vector_embeddings = []
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    for row in db_data:
        article_links.append(row.link_to_article)

    article_description, article_keywords, article_title = extract_metadata(article_links)

    for article in article_description:
        vector_embeddings.append(embeddings.embed_query(article))

    
    company = []
    location = []
    company_stock_symbol = []
    closing_price = []
    volume = []

    sentiment_score = []

    for row in db_data:
        title = row.title
        link_to_article = row.link_to_article
        snippet = row.snippet
        tags = row.snippet
        source = row.source
        date_of_news = row.date_of_news
        
        company_temp, location_temp = llm_response(title, link_to_article, snippet, tags, source)
        company.append(company_temp)
        location.append(location_temp)
        
        if company_temp != 'None':
            closing_price_temp, volume_temp = stock_extraction(company_temp, date_of_news)
            closing_price.append(closing_price_temp)
            volume.append(volume_temp)
        else:
            closing_price.append(None)
            volume.append(None)
            
        blob = TextBlob(row.snippet)
        sentiment = blob.sentiment.polarity
        sentiment_score.append(sentiment)
        
    
    for i, row in enumerate(db_data, start=0):
                
        new_entry = SerpTest(position_in_search = row.position_in_search, date_of_news = row.date_of_news, title = row.title, link_to_article = row.link_to_article, snippet = article_description[i], tags= article_keywords[i], source = row.source, vectors = vector_embeddings[i], company = company[i], location = location[i], closing_price = closing_price[i], volume = volume[i], sentiment = sentiment_score[i])
        
        # Add the new entry to the session
        db.session.add(new_entry)
        
        db.session.commit() 
        
    db.session.close()

        
        
    # print(company)
    # print("---------")
    # print(location)
    
    

if __name__ == '__main__':
    
    app.run()