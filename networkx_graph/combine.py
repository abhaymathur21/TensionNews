from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
import networkx as nx
import json
from sqlalchemy.dialects.postgresql import JSONB
import community
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.bmkjkdaiqpvixkkjdlhp:TensionFlowLOC@aws-0-ap-south-1.pooler.supabase.com:5432/postgres'
db = SQLAlchemy(app)

CORS(app)

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
    tags = db.Column(JSONB)

def tag_similarity():
    print("tag!")
    tags = db.session.query(SerpTest.tags).all()
    num_rows = len(tags)
    similarity_matrix= np.zeros((num_rows, num_rows))
    for i in range(num_rows):
        for j in range(num_rows):
            tag1 = tags[i]
            tag2 = tags[j]
            similarity_matrix[i][j] = calculate_tag_similarity(tag1, tag2)
            
    # print("Similarity_Matrix: ", similarity_matrix.tolist())
    return Graph_networkx(0.2,num_rows,similarity_matrix)
    # return jsonify({"Similarity_Matrix": similarity_matrix.tolist()}), 200

def calculate_tag_similarity(tags1, tags2):
    tags1_list = tags1[0].split(",") if tags1 else []
    tags2_list = tags2[0].split(",") if tags2 else []
    
    # print("Tags1:", tags1_list)
    # print("Tags2:", tags2_list)
    
    if not tags1_list or not tags2_list:
        # print("One of the tag lists is empty.")
        return 0 
    
    common_tags = len(set(tags1_list) & set(tags2_list)) 
    # print("Common Tags:", common_tags)
    
    similarity = common_tags / len(tags1_list)
    # print("Similarity:", similarity)
    
    return similarity

def calculate_vector_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)
    similarity = dot_product / (norm_vector1 * norm_vector2)
    return similarity

def vector_similarity():
    vectors = db.session.query(SerpTest.vectors).all()
    vectors = [np.array(vector[0]) for vector in vectors]
    
    num_rows = len(vectors)
    
    similarity_matrix = np.zeros((num_rows, num_rows))
    for i in range(num_rows):
        for j in range(num_rows):
            vector1 = vectors[i]
            vector2 = vectors[j]
            if isinstance(vector1, dict):
                vector1 = np.array(vector1['vectors']) 
            if isinstance(vector2, dict):
                vector2 = np.array(vector2['vectors'])  
            similarity_matrix[i, j] = calculate_vector_similarity(vector1, vector2)
    return Graph_networkx(0.5,num_rows,similarity_matrix)
    
    # return jsonify({"Similarity_Matrix": similarity_matrix.tolist()})



def Graph_networkx(threshold, num_rows,similarity_matrix):
    title = db.session.query(SerpTest.title).all()
    G = nx.Graph()
    for i in range(num_rows):
        G.add_node(i + 1, id=i + 1, title = title[i])
    
    for i in range(num_rows):
        for j in range(i + 1, num_rows):
            similarity = similarity_matrix[i, j]
            if threshold < similarity < 1:
                G.add_edge(i + 1, j + 1, weight=similarity)

    partition = community.best_partition(G)
    for node_id, cluster_id in partition.items():
        G.nodes[node_id]['cluster'] = cluster_id

    data1 = nx.node_link_data(G)
    json_filename = 'graph_data_from_flask.json'
    data1['clusters'] = {"Clusters": partition}
    
    with open(json_filename, 'w') as json_file:
        json.dump(data1, json_file, indent=2)

    return jsonify({"Similarity_Matrix": similarity_matrix.tolist(), "Graph_Data": data1, "Cluster_Data": {"Clusters": partition}}), 200


@app.route('/graph/<type>')
def graph(type):
    
    if type=='tag':
        print("Tag")
        return tag_similarity()
    elif type=='overall':
        print("overall")
        return vector_similarity()
    else:
        return {}
if __name__ == '__main__':
    # with app.app_context():
    #     query=input('Enter the variable: ')
    #     if query=='tag':
    #         tag_similarity()
    #     if query=='vector':
    #         vector_similarity()
    app.run(debug=True)
