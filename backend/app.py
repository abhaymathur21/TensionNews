from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from sqlalchemy.dialects.postgresql import ARRAY
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.bmkjkdaiqpvixkkjdlhp:TensionFlowLOC@aws-0-ap-south-1.pooler.supabase.com:5432/postgres'

db.init_app(app)
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
    source = db.Column(db.String)
    vectors = db.Column(db.JSON)

with open('backend/google_serp_api.json', 'r') as file:
    data = json.load(file)
    # for entry in data:
    #     print(entry)
    
article_links = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
  }

for entry in data:
    article_links.append(entry["link"])
    
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
        # print(description)
        
    keywords_meta_tag = soup_.find('meta', attrs={'name': 'keywords'})
    if keywords_meta_tag:
        keywords = keywords_meta_tag.get('content')
        article_keywords.append(keywords)
        # print(keywords)


vector_embeddings = []
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


for entry in data:
    vector_embeddings.append(embeddings.embed_query(entry["snippet"]))

# for vector in vector_embeddings:
#     print(vector)
# print(vector_embeddings[0])

if __name__ == '__main__':
    
    # with app.app_context():
                        
    #     db.create_all()    
        
    #     for i, entry in enumerate(data, start=0):
    #         # Create a new SerpTest object for each entry
            
            
            
    #         new_entry = SerpTest(source_json=entry, position_in_search = entry["position"], title = entry["title"], link_to_article = entry["link"], snippet = entry["snippet"], source = entry["source"], vectors = vector_embeddings[i])
            
    #         # Add the new entry to the session
    #         db.session.add(new_entry)
            
    #         db.session.commit()
                
    #     db.session.close()


    app.run()