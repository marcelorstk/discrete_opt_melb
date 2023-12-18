import random
from typing import List
import networkx as nx
from ortools.sat.python import cp_model

from aux import to_network, sort_node_by_degree

# Global constants
MAIN_SOLVER_TIME = 120

def solver(edges: List[tuple], node_count: int, use_clique: bool = True) -> list:
    """
    I'll solve the coloring graph problem (https://en.wikipedia.org/wiki/Graph_coloring)
    with ortools by google (https://developers.google.com/optimization/cp)
    Also, I've used the idea of using the cliques of a graph to add redundant constraints 
    from this article ("Exact Solution of Graph Coloring Problems via Constraint
    Programming and Column Generation - "https://optimization-online.org/wp-content/uploads/2010/03/2568.pdf)
    The formulation is good enough to find adequate solutions, but improve needed, especially when dealing with 100+ highly connected nodes

    Args:
        edges (List[tuple]): List of graph's edges
        node_count (int): Number of nodes

    Returns:
        list: List of colors of each node
    """    
    # MODEL
    model = cp_model.CpModel()

    # PRE-PROCESSING
    # Get a set of cliques from the graph
    if use_clique:
        cliques = _get_set_cliques(edges, node_count, n_tries=5)
        # Select the longest clique
        max_len_clique = max([len(x) for x in cliques])
        filt_clique = list(filter(lambda x: len(x)==max_len_clique, cliques))[0]
        # Nodes will be (Nodes inside clique + rest of nodes in order)
        nodes_list = filt_clique + [node for node in range(node_count) if node not in filt_clique]

    else:
        # On this case I'll order the nodes by their number of edges
        nodes_list, _ = sort_node_by_degree(edges, node_count)
        filt_clique = list()

    # VARIABLES
    # Nodes -> Use Symmetry Breaking
    # Since the nodes from a same clique must have different colors, we'll assign fixed values to them
    # Next nodes we'll just add+1 on the possibilities (E.g Node N have N+1 possible colors [N from previous + 1 for itself])
    nodes = list()
    for rank, node in enumerate(nodes_list):
        if node in filt_clique:
            nodes.append(
                model.NewIntVar(rank, rank, f"Node {node}")
            )
        else:
            nodes.append(
                model.NewIntVar(0, rank, f"Node {node}")
            )

    # CONSTRAINTS
    ## Adjacente nodes must be different one by one
    for i,j in edges:
        model.Add(nodes[nodes_list.index(i)] != nodes[nodes_list.index(j)])
    ## Colors on the same clique must be all differents
    if use_clique:
        for clique in cliques:
            _nodes = [nodes[nodes_list.index(i)] for i in clique]
            model.AddAllDifferent(_nodes)

    # OBJECTIVE FUNCTION
    ## Objetive function is the max number of the nodes
    obj_func = model.NewIntVar(0, node_count-1, "Max color")
    model.AddMaxEquality(target=obj_func, exprs=nodes)
    # Minimize objetive
    model.Minimize(obj_func)

    # SOLVE
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = MAIN_SOLVER_TIME
    solver.parameters.num_search_workers = 16
    solver.optimize_with_core = True
    solver.Solve(model)

    # COLORS
    ordered_nodes = sorted(nodes, key=lambda x: nodes_list[x.Index()])
    colors = [solver.Value(node) for node in ordered_nodes]

    return colors


def _get_set_cliques(orig_edges: list, node_count: int, n_tries: int = 3) -> list:
    _, g = to_network(edges=orig_edges, node_count=node_count)
    g_compl = nx.complement(g)

    cliques_list = list()
    for i in range(n_tries):
        nodes_list = [i for i in g_compl.nodes]
        edges = [i for i in g_compl.edges]
        random.shuffle(nodes_list)

        # Solve color problem 
        aux_model = cp_model.CpModel()

        nodes = [
            aux_model.NewIntVar(0, i, f"Edge {edge}") for i, edge in enumerate(nodes_list)
        ]
        obj_func = aux_model.NewIntVar(0, node_count-1, "Max color")
        aux_model.AddMaxEquality(target=obj_func, exprs=nodes)

        for i,j in edges:
            aux_model.Add(nodes[nodes_list.index(i)] != nodes[nodes_list.index(j)])

        aux_model.Minimize(obj_func)

        aux_solver = cp_model.CpSolver()
        aux_solver.parameters.max_time_in_seconds = 60
        aux_solver.parameters.num_search_workers = 16
        aux_solver.optimize_with_core = True
        aux_solver.Solve(aux_model)

        ordered_nodes = sorted(nodes, key=lambda x: nodes_list[x.Index()])
        colors = [aux_solver.Value(node) for node in ordered_nodes]

        # color_nodes_dict = dict()
        for color in set(colors):
            clique = [i for i, col in enumerate(colors) if col==color]
            if len(clique) > 2:
                cliques_list.append(clique)

    return cliques_list
