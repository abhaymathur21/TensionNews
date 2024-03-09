from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
import networkx as nx
import json
import community  # Louvain community detection

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
    return similarity

def calculate_similarity():
    # Fetch vectors from the database
    vectors = db.session.query(SerpTest.vectors).all()
    vectors = [np.array(vector[0]) for vector in vectors]
    
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
    Graph_networkx(0.5,num_rows,similarity_matrix)
    # Generate a new semantic network based on the similarity matrix
def Graph_networkx(threshold, num_rows,similarity_matrix):
    G = nx.Graph()
    for i in range(num_rows):
        G.add_node(i + 1, id=i + 1)  # Add nodes with generated IDs
    
    for i in range(num_rows):
        for j in range(i + 1, num_rows):
            similarity = similarity_matrix[i, j]
            if threshold < similarity < 1:
                G.add_edge(i + 1, j + 1, weight=similarity)

    # Perform Louvain clustering
    partition = community.best_partition(G)
    
    # Add cluster information to graph data
    for node_id, cluster_id in partition.items():
        G.nodes[node_id]['cluster'] = cluster_id

    data1 = nx.node_link_data(G)
    json_filename = 'graph_data_from_flask.json'
    
    # Add cluster data to graph data
    data1['clusters'] = {"Clusters": partition}
    
    with open(json_filename, 'w') as json_file:
        json.dump(data1, json_file, indent=2)

    return jsonify({"Similarity_Matrix": similarity_matrix.tolist(), "Graph_Data": data1, "Cluster_Data": {"Clusters": partition}}), 200

if __name__ == '__main__':
    with app.app_context():
        calculate_similarity()
    app.run(debug=True)
