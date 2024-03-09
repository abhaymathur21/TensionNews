from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from sqlalchemy.dialects.postgresql import JSONB
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

from llm import llm_response
from metadata import extract_metadata

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.bmkjkdaiqpvixkkjdlhp:TensionFlowLOC@aws-0-ap-south-1.pooler.supabase.com:5432/postgres'

# Define your models here

class SerpTest(db.Model):
    __tablename__ = 'SerpTest'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    source_json = db.Column(db.JSON)
    position_in_search = db.Column(db.Integer)
    title = db.Column(db.String)
    link_to_article = db.Column(db.String)
    snippet = db.Column(db.String)
    tags = db.Column(JSONB)
    source = db.Column(db.String)
    vectors = db.Column(db.JSON)
    
db.init_app(app)

with open('backend/google_serp_api.json', 'r') as file:
    data = json.load(file)

article_links = []
vector_embeddings = []
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

for entry in data:
    article_links.append(entry["link"])

article_description, article_keywords, article_title = extract_metadata(article_links)

for article in article_description:
    vector_embeddings.append(embeddings.embed_query(article))
    
# TO ADD NEW ENTRIES TO THE DATABASE, UNCOMMENT THE FOLLOWING CODE:  
    
# with app.app_context():
#     db.create_all()        
    
#     for i, entry in enumerate(data, start=0):
                
#         new_entry = SerpTest(source_json=entry, position_in_search = entry["position"], title = entry["title"], link_to_article = entry["link"], snippet = article_description[i], tags= article_keywords[i], source = entry["source"], vectors = vector_embeddings[i])
        
#         # Add the new entry to the session
#         db.session.add(new_entry)
        
#         db.session.commit() 
        
#     db.session.close()
    
    
with app.app_context():    
    company = []
    location = []

    db_data = SerpTest.query.all()

    for row in db_data:
        title = row.title
        link_to_article = row.link_to_article
        snippet = row.snippet
        tags = row.snippet
        source = row.source
        
        company_temp, location_temp = llm_response(title, link_to_article, snippet, tags, source)
        company.append(company_temp)
        location.append(location_temp)
        
    print(company)
    print("---------")
    print(location)

if __name__ == '__main__':
    
    app.run()