import networkx as nx

import pandas as pd

def compute_centrality(G):
    """
    Compute several centrality measures for a graph.

    Returns
    -------
    DataFrame
        One row per taxon.
    """

    degree = nx.degree_centrality(G)

    betweenness = nx.betweenness_centrality(
        G,
        normalized=True,
    )

    eigenvector = nx.eigenvector_centrality(
        G,
        max_iter=1000,
    )
    df = pd.DataFrame({
        "Taxon": degree.keys(),
        "Degree": degree.values(),
        "Betweenness": betweenness.values(),
        "Eigenvector": eigenvector.values(),
    })

    df = df.sort_values(
        "Degree",
        ascending=False,
    ).reset_index(drop=True)

    df["Rank"] = range(
        1,
        len(df) + 1,
    )

    return df
