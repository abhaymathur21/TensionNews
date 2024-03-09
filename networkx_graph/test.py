import networkx as nx
import matplotlib.pyplot as plt
import requests
import json
import numpy as np

def fetch_news_data():
    news_data = [
        {'id': 1, 'title': 'Article 1', 'image_url': 'url_1'},
        {'id': 2, 'title': 'Article 2', 'image_url': 'url_2'},
        {'id': 3, 'title': 'Article 3', 'image_url': 'url_3'},
        {'id': 4, 'title': 'Article 4', 'image_url': 'url_4'},
        {'id': 5, 'title': 'Article 5', 'image_url': 'url_5'},
        {'id': 6, 'title': 'Article 6', 'image_url': 'url_6'},
        {'id': 7, 'title': 'Article 7', 'image_url': 'url_7'},
        {'id': 8, 'title': 'Article 8', 'image_url': 'url_8'},
        {'id': 9, 'title': 'Article 9', 'image_url': 'url_9'},
        {'id': 10, 'title': 'Article 10', 'image_url': 'url_10'}
    ]

    return news_data

def create_semantic_network(news_data, similarity_matrix):
    G = nx.Graph()
    for article in news_data:
        article_id = article['id']
        G.add_node(article_id, title=article['title'], image_url=article['image_url'])

    for i in range(len(news_data)):
        for j in range(i + 1, len(news_data)):
            similarity = similarity_matrix[i, j]
            if 0.5 < similarity < 1:
                G.add_edge(news_data[i]['id'], news_data[j]['id'], weight=similarity)

    data1 = nx.node_link_data(G)
    json_filename = 'graph_data.json'
    with open(json_filename, 'w') as json_file:
        json.dump(data1, json_file, indent=2)

    return G

# Dummy similarity matrix (replace this with your actual matrix)
dummy_similarity_matrix = np.random.rand(10, 10)  # 10x10 matrix with random values
np.fill_diagonal(dummy_similarity_matrix, 1.0)  # Set diagonal elements to 1

news_data = fetch_news_data()
semantic_network = create_semantic_network(news_data, dummy_similarity_matrix)
edge_widths = [semantic_network[u][v]['weight'] * 3 for u, v in semantic_network.edges()]
layout = nx.spring_layout(semantic_network)
plt.figure(figsize=(10, 8))
nx.draw(semantic_network, pos=layout, with_labels=False, node_size=800, node_color='skyblue', width=edge_widths, edge_color='gray')

node_labels = {node_id: f"{node_id}: {semantic_network.nodes[node_id]['title']}" for node_id in semantic_network.nodes}
nx.draw_networkx_labels(semantic_network, pos=layout, labels=node_labels, font_size=10)

plt.title('Semantic Network of News Articles')
plt.show()
