import networkx as nx
import random as random
import matplotlib.pyplot as plt

# fonction permettant de générer un graphe en grille aléatoire avec perturbation d'arête
# n indique le nombre de noeuds au carré
# la variable coef suppr détermine le coefficient de suppression des arêtes
# la variable show indique si il faut afficher le graphe ou non
def generate_2D_graph(n, coef_suppr=False, show=False):
    graph = nx.grid_2d_graph(n, n)  # n x n grid

    if coef_suppr != False:
        nb_suppr = int(len(list(graph.nodes)) * coef_suppr)

        random_edge(graph, nb_suppr, delete=True)

    pos = nx.spring_layout(graph, iterations=100)

    graph.remove_nodes_from(list(nx.isolates(graph)))
    graph = graph.to_directed()

    if show:
        nx.draw(graph, pos, node_color='b', node_size=20, with_labels=False)
        plt.title("Road network")
        plt.show()

    return graph


# ajoute ou supprime un nombre d'arêtes dans un graphe
def random_edge(graph, nb_edges, delete=True):
    edges = list(graph.edges)
    nonedges = list(nx.non_edges(graph))

    # random edge choice
    if delete:
        # delete chosen edge
        chosen_edges = random.sample(edges, nb_edges)
        for edge in chosen_edges:
            graph.remove_edge(edge[0], edge[1])
    # add new edge
    else:
        chosen_nonedges = random.sample(nonedges, nb_edges)
        for non_edge in chosen_nonedges:
            graph.add_edge(non_edge[0], non_edge[1])

    return graph