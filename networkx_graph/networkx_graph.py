import networkx as nx
import matplotlib.pyplot as plt
import requests
import json
# Function to fetch news articles and images from an API
def fetch_news_data():
    news_data = [
        {
            'id': 1,
            'title': 'Example Article 1',
            'image_url': 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.reddit.com%2Fr%2FPixelArt%2Fcomments%2F15z47dt%2Fi_got_bored_so_i_decided_to_draw_a_random_image%2F&psig=AOvVaw3WCJMGx9Ze-2jNNiN6bem3&ust=1710063180858000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCNih5PXv5oQDFQAAAAAdAAAAABAE'
        },
        {
            'id': 2,
            'title': 'Example Article 2',
            'image_url': 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.reddit.com%2Fr%2FPixelArt%2Fcomments%2F15z47dt%2Fi_got_bored_so_i_decided_to_draw_a_random_image%2F&psig=AOvVaw3WCJMGx9Ze-2jNNiN6bem3&ust=1710063180858000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCNih5PXv5oQDFQAAAAAdAAAAABAE'
        },
        {
            'id': 3,
            'title': 'Example Article 3',
            'image_url': 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.reddit.com%2Fr%2FPixelArt%2Fcomments%2F15z47dt%2Fi_got_bored_so_i_decided_to_draw_a_random_image%2F&psig=AOvVaw3WCJMGx9Ze-2jNNiN6bem3&ust=1710063180858000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCNih5PXv5oQDFQAAAAAdAAAAABAE'
        }
    ]
    
    return news_data

def compute_similarity(article1, article2):
    w = 1
    return w

# Function to create semantic network
def create_semantic_network(news_data):
    G = nx.Graph()

    # Add nodes (news articles) to the graph
    for article in news_data:
        article_id = article['id']
        G.add_node(article_id, title=article['title'], image_url=article['image_url'])

    # Add edges with similarity scores
    for i in range(len(news_data)):
        for j in range(i + 1, len(news_data)):
            similarity = compute_similarity(news_data[i], news_data[j])
            if similarity > 0:  # Include only non-zero similarity edges
                G.add_edge(news_data[i]['id'], news_data[j]['id'], weight=similarity)

    return G

# Export graph data to JSON
def export_graph_to_json(graph, filename):
    graph_data = {
        'nodes': [],
        'edges': []
    }

    for node_id, node_attrs in graph.nodes(data=True):
        graph_data['nodes'].append({
            'id': node_id,
            'title': node_attrs['title'],
            'image_url': node_attrs['image_url']
        })

    for u, v, edge_attrs in graph.edges(data=True):
        graph_data['edges'].append({
            'source': u,
            'target': v,
            'weight': edge_attrs['weight']
        })

    with open(filename, 'w') as json_file:
        json.dump(graph_data, json_file, indent=2)

# Fetch news data from the API
news_data = fetch_news_data()

# Create semantic network
semantic_network = create_semantic_network(news_data)

# Set edge thickness based on similarity score
edge_widths = [semantic_network[u][v]['weight'] * 3 for u, v in semantic_network.edges()]

# Choose a layout for the graph
layout = nx.spring_layout(semantic_network)

# Draw the graph
plt.figure(figsize=(10, 8))
nx.draw(semantic_network, pos=layout, with_labels=False, node_size=800, node_color='skyblue', width=edge_widths, edge_color='gray')

# Add node labels (ID and article title)
node_labels = {node_id: f"{node_id}: {semantic_network.nodes[node_id]['title']}" for node_id in semantic_network.nodes}
nx.draw_networkx_labels(semantic_network, pos=layout, labels=node_labels, font_size=10)

plt.title('Semantic Network of News Articles')
plt.show()

# Export graph to a new JSON file
export_graph_to_json(semantic_network, 'new_semantic_network_data.json')