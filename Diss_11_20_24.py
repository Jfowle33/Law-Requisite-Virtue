# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 10:08:49 2024

@author: JoeCF
"""

import networkx as nx
import pandas as pd
import numpy as np
import itertools

# Load the Excel file
file_path = 'D:/10192024_Vote_Bill_pos_contr.xlsx'
xls = pd.read_excel(file_path)

# Display the first few rows to understand the structure
print(xls.head())

xls['Contribution_Amount'] = pd.to_numeric(xls['Contribution_Amount'], errors='coerce')

# Filter data for relevant PACs associated with the "Tax Cuts and Jobs Act"
relevant_pacs = [
    'Other single-issue or ideological groups',
    'Democratic/Liberal',
    'Republican/Conservative'
]
filtered_data = xls[xls['PAC_Name'].isin(relevant_pacs)]

# Summarize contributions by PAC and voting behavior (Yea/Nay)
analysis = filtered_data.groupby(['PAC_Name', 'Vote']).agg(
    Total_Contributions=('Contribution_Amount', 'sum'),
    Average_Contribution=('Contribution_Amount', 'mean'),
    Contribution_Count=('Contribution_Amount', 'count')
).reset_index()

# Display the results for further analysis
import matplotlib.pyplot as plt

# Initialize a new graph to include senators
G = nx.Graph()

# Add PAC nodes
for pac in filtered_data['PAC_Name'].unique():
    G.add_node(pac, type='PAC', color='gray')

# Add senator nodes with party affiliation
senators = filtered_data[['Senator_ID', 'Party']].drop_duplicates()
party_colors = {'D': 'blue', 'R': 'red'}  # Democrat: blue, Republican: red
for _, row in senators.iterrows():
    G.add_node(row['Senator_ID'], type='Senator', color=party_colors.get(row['Party'], 'green'))

# Add vote nodes
for vote in filtered_data['Vote'].unique():
    G.add_node(vote, type='Vote', color='orange')

# Add edges: PAC -> Senator and Senator -> Vote
for _, row in filtered_data.iterrows():
    G.add_edge(row['PAC_Name'], row['Senator_ID'], weight=row['Contribution_Amount'])
    G.add_edge(row['Senator_ID'], row['Vote'], weight=1)

# Assign colors for visualization
node_colors = [data['color'] for _, data in G.nodes(data=True)]

# Draw the network
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, seed=42)  # Layout for consistent visualization
nx.draw_networkx_nodes(G, pos, node_size=500, node_color=node_colors)
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=8)

plt.title("Network of PACs, Senators, and Votes")
plt.axis('off')
plt.show()

# Calculate centrality measures for PAC nodes
pac_nodes = [n for n, attr in G.nodes(data=True) if attr['type'] == 'PAC']

# Degree centrality
degree_centrality = nx.degree_centrality(G)
pac_degree_centrality = {node: degree_centrality[node] for node in pac_nodes}

# Betweenness centrality
betweenness_centrality = nx.betweenness_centrality(G, normalized=True, weight='weight')
pac_betweenness_centrality = {node: betweenness_centrality[node] for node in pac_nodes}



# Since eigenvector centrality failed, we'll only use degree and betweenness centrality
influential_pacs = pd.DataFrame({
    'PAC_Name': pac_nodes,
    'Degree_Centrality': [pac_degree_centrality[pac] for pac in pac_nodes],
    'Betweenness_Centrality': [pac_betweenness_centrality[pac] for pac in pac_nodes],
})

# Bar chart to compare centrality measures of PACs
plt.figure(figsize=(10, 6))
influential_pacs.set_index('PAC_Name')[['Degree_Centrality', 'Betweenness_Centrality']].plot(
    kind='bar', figsize=(10, 6), alpha=0.75
)

plt.title("Centrality Measures of PACs")
plt.ylabel("Centrality Score")
plt.xlabel("PAC Name")
plt.xticks(rotation=45, ha='right')
plt.legend(title="Centrality Type")
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


# Split the network data by vote (Yea or Nay)
yes_votes = filtered_data[filtered_data['Vote'] == 'Yea']
no_votes = filtered_data[filtered_data['Vote'] == 'Nay']

# Create separate networks for Yes and No votes
def build_pac_vote_network(data):
    G = nx.Graph()
    for pac in data['PAC_Name'].unique():
        G.add_node(pac, type='PAC', color='gray')
    for _, row in data.iterrows():
        G.add_node(row['Senator_ID'], type='Senator', color=party_colors.get(row['Party'], 'green'))
        G.add_node(row['Vote'], type='Vote', color='orange')
        G.add_edge(row['PAC_Name'], row['Senator_ID'], weight=row['Contribution_Amount'])
        G.add_edge(row['Senator_ID'], row['Vote'], weight=1)
    return G

# Build separate graphs for Yes and No votes
yes_vote_network = build_pac_vote_network(yes_votes)
no_vote_network = build_pac_vote_network(no_votes)

# Calculate centrality for Yes and No networks
def calculate_pac_centrality(graph, pac_nodes):
    degree_centrality = nx.degree_centrality(graph)
    betweenness_centrality = nx.betweenness_centrality(graph, normalized=True, weight='weight')
    return pd.DataFrame({
        'PAC_Name': pac_nodes,
        'Degree_Centrality': [degree_centrality.get(pac, 0) for pac in pac_nodes],
        'Betweenness_Centrality': [betweenness_centrality.get(pac, 0) for pac in pac_nodes],
    })

# Get PAC nodes for both networks
pac_nodes_yes = [n for n, attr in yes_vote_network.nodes(data=True) if attr['type'] == 'PAC']
pac_nodes_no = [n for n, attr in no_vote_network.nodes(data=True) if attr['type'] == 'PAC']

# Calculate centrality for each network
yes_centrality = calculate_pac_centrality(yes_vote_network, pac_nodes_yes)
no_centrality = calculate_pac_centrality(no_vote_network, pac_nodes_no)

# Combine the results for comparison
centrality_comparison = yes_centrality.merge(
    no_centrality, on='PAC_Name', suffixes=('_Yes', '_No')
)

# Create a side-by-side bar chart for "Yes" and "No" votes
fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# Plot degree centrality
centrality_comparison.set_index('PAC_Name')[['Degree_Centrality_Yes', 'Degree_Centrality_No']].plot(
    kind='bar', ax=axes[0], alpha=0.75
)
axes[0].set_title("Degree Centrality: Yes vs No Votes")
axes[0].set_ylabel("Centrality Score")
axes[0].legend(title="Vote")

# Plot betweenness centrality
centrality_comparison.set_index('PAC_Name')[['Betweenness_Centrality_Yes', 'Betweenness_Centrality_No']].plot(
    kind='bar', ax=axes[1], alpha=0.75
)
axes[1].set_title("Betweenness Centrality: Yes vs No Votes")
axes[1].set_ylabel("Centrality Score")
axes[1].legend(title="Vote")

plt.xlabel("PAC Name")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
