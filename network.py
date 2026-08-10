import networkx as nx
import numpy as np

def correlation_matrix(abundance, method="spearman"):
    """
    Compute taxon-by-taxon correlation matrix.
    """

    return abundance.T.corr(method=method)


def build_network(corr, threshold=0.5):
    """
    Build an undirected network from
    a correlation matrix.
    """

    G = nx.Graph()

    taxa = corr.index

    for i in range(len(taxa)):
        for j in range(i + 1, len(taxa)):

            weight = corr.iloc[i, j]

            if abs(weight) >= threshold:

                G.add_edge(
                    taxa[i],
                    taxa[j],
                    weight=weight
                )

    return G

def build_network_from_edges(
    edges,
    taxa,
    weight_column="weight",
):

    G = nx.Graph()

    G.add_nodes_from(taxa)

    for _, row in edges.iterrows():

        if row["significant"]:

            G.add_edge(
                row["taxon1"],
                row["taxon2"],
                weight=row[weight_column],
            )

    return G

def network_summary(G, method):
    """
    Compute and print a summary of a NetworkX graph.
    Returns a dictionary of summary statistics.
    """

    n_nodes = G.number_of_nodes()
    n_edges = G.number_of_edges()

    if n_nodes == 0:
        print("Graph is empty.")
        return None

    density = nx.density(G)

    degrees = [d for _, d in G.degree()]
    avg_degree = np.mean(degrees)

    components = list(nx.connected_components(G))

    summary = {
        "Method": method,
        "Nodes": n_nodes,
        "Edges": n_edges,
        "Density": density,
        "Average Degree": avg_degree,
        "Maximum Degree": max(degrees),
        "Minimum Degree": min(degrees),
        "Connected Components": len(components),
        "Largest Component": len(max(components, key=len)),
        "Average Clustering": nx.average_clustering(G)
    }

    print("=" * 40)
    print("Network Summary")
    print("=" * 40)

    for key, value in summary.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")

    print("=" * 40)

    return summary