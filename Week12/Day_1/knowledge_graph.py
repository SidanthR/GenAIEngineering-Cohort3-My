import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

# Load data
movie_data = pd.read_csv('imdb.csv', nrows=200)

# Initialize the graph
G = nx.Graph()

# Define a function to add edges
def add_edges(graph, source, targets, weight, source_type, target_type):
    for target in targets:
        graph.add_node(source, type=source_type)
        graph.add_node(target, type=target_type)
        graph.add_edge(source, target, weight=weight)

# Process each movie
for _, row in movie_data.iterrows():
    title = row['Title']
    director = row['Director']
    genres = row['Genre'].split(',')
    actors = row['Actors'].split(', ')
    weight = row['Rating']  # You can change this to 'Revenue (Millions)' for revenue-based weights
    
    # Add edges for directors, genres, and actors
    add_edges(G, title, [director], weight, 'Movie', 'Director')
    add_edges(G, title, genres, weight, 'Movie', 'Genre')
    add_edges(G, title, actors, weight, 'Movie', 'Actor')

# Draw the graph
plt.figure(figsize=(20, 15))
layout = nx.spring_layout(G, k=0.15, iterations=20)

# Colors
colors = {'Movie': 'lightblue', 'Director': 'orange', 'Genre': 'green', 'Actor': 'red'}

# Draw nodes
for node, (x, y) in layout.items():
    node_type = G.nodes[node]['type']
    color = colors[node_type]
    plt.scatter(x, y, c=color, s=100, edgecolors='k', label=node_type if node_type not in plt.gca().get_legend_handles_labels()[1] else "")

# Draw edges
nx.draw_networkx_edges(G, pos=layout, alpha=0.3)

# Draw labels
for node, (x, y) in layout.items():
    plt.text(x, y, s=node, fontsize=8, ha='right' if node_type == 'Movie' else 'left')

plt.title('IMDB Movie Knowledge Graph')
plt.legend()
plt.axis('off')
plt.savefig('imdb_knowledge_graph.png')
plt.show()