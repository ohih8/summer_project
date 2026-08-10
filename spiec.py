import pandas as pd
import networkx as nx


def load_spiec_network(edge_file):
    """
    Load a SPIEC-EASI edge list exported from R.
    """

    edges = pd.read_csv(edge_file)

    G = nx.Graph()

    for _, row in edges.iterrows():
        G.add_edge(
            row["taxon1"],
            row["taxon2"],
            weight=1.0
        )

    return G