import pandas as pd

from preprocessing import (
    relative_abundance,
    clr_transform,
    prevalence_filter,
)

from association import (
    pairwise_correlation,
)

from network import (
    build_network_from_edges,
    network_summary,
)

from centrality import (
    compute_centrality,
)

from degree import(
    degree_distribution,
)

def run_pipeline(
    abundance,
    transform="relative",
    association="spearman",
    prevalence=0.10,
):
    """
    Run one complete network inference pipeline.
    """

    abundance = prevalence_filter(
        abundance,
        prevalence,
    )

    abundance = relative_abundance(
        abundance,
    )

    if transform == "clr":

        abundance = clr_transform(
            abundance,
        )

    if association not in (
        "spearman",
        "pearson",
    ):
        raise ValueError(
            "Unknown association method."
        )

    edges = pairwise_correlation(
        abundance,
        method=association,
    )

    G = build_network_from_edges(
        edges,
        abundance.index,
    )

    method_name = f"{transform}_{association}"

    summary = network_summary(
        G,
        method=method_name,
    )

    centrality = compute_centrality(G)

    degrees = degree_distribution(G)

    return {
        "graph": G,
        "edges": edges,
        "summary": summary,
        "centrality": centrality,
        "degrees": degrees,
    }

def analyze_existing_graph(
    graph,
    method,
    edges_path,
):

    summary = network_summary(
        graph,
        method=method,
    )

    centrality = compute_centrality(
        graph,
    )

    degrees = degree_distribution(
        graph,
    )

    edges = pd.read_csv(
        edges_path,
    )

    return {
        "graph": graph,
        "edges": edges,
        "summary": summary,
        "centrality": centrality,
        "degrees": degrees,
    }