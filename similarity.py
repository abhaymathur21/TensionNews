from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime

app = Flask(__name__)

# Initialize SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.bmkjkdaiqpvixkkjdlhp:TensionFlowLOC@aws-0-ap-south-1.pooler.supabase.com:5432/postgres'
db = SQLAlchemy(app)

# Define your model
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

# Function to compute cosine similarity
def compute_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)
    similarity = dot_product / (norm_vector1 * norm_vector2)
    # print(similarity)
    return similarity

def calculate_similarity():
    print("hello")
    # Fetch vectors from the database
    vectors = db.session.query(SerpTest.vectors).all()
    vectors = [np.array(vector[0]) for vector in vectors]
    # print(vectors)

    
    num_rows = len(vectors)
    
    # Calculate cosine similarity between vectors
    similarity_matrix = np.zeros((num_rows, num_rows))
    for i in range(num_rows):
        for j in range(num_rows):
            vector1 = vectors[i]
            vector2 = vectors[j]
            if isinstance(vector1, dict):
                vector1 = np.array(vector1['vectors'])  # Convert dictionary to NumPy array
            if isinstance(vector2, dict):
                vector2 = np.array(vector2['vectors'])  # Convert dictionary to NumPy array
            similarity_matrix[i, j] = compute_similarity(vector1, vector2)
    print("Similarity_Matrix: ", similarity_matrix.tolist())

    return jsonify({"Similarity_Matrix": similarity_matrix.tolist()}), 200

if __name__ == '__main__':
    with app.app_context():
        calculate_similarity()
    app.run(debug=True)
    
