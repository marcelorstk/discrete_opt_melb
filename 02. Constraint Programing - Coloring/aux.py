from typing import Tuple, List
import networkx as nx
from pyvis.network import Network


def to_network(edges: List[tuple], node_count: int, colors: list = None) -> Tuple[Network, nx.graph.Graph]:
    """
    Function to create a graph based on edges and number of nodes

    Args:
        edges (List[tuple]): List of tuples of the graphs edges 
        node_count (int): Number of nodes in the graph
        colors (list, optional): Colors of the nodes if we have it. Defaults to None.
    """    
    # Generate basis for the plot
    g_plot = Network(notebook=True, cdn_resources="remote")
    g_plot.repulsion()
    
    # Generate graph
    g = nx.graph.Graph()
    for node in range(node_count):
        color = 0
        if colors:
            color = colors[node]
        g.add_node(node, title=f"Node {node}", group=color)
    
    for edge in edges:
        g.add_edge(edge[0], edge[1])
    
    # Transform to pyvis
    g_plot.from_nx(g)
    
    return g_plot, g



def sort_node_by_degree(edges: list, node_count: int) -> Tuple[list]:
    """
    Sort graphs nodes by the number of edges that it have
    """
    node_degree_list = list()
    for node in range(node_count):
        set_adj_nodes = set([i for edge in edges for i in edge if node in edge])
        degree = len(set_adj_nodes) - 1
        node_degree_list.append((node, degree))
    node_degree_list = sorted(node_degree_list, key=lambda x: x[1], reverse=True)
    node_list = [i[0] for i in node_degree_list]
    return node_list, node_degree_list