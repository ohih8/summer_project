from pathlib import Path
import networkx as nx
import pandas as pd

from preprocessing import (
    load_data,
    prevalence_filter,
)
from pipeline import (
    run_pipeline,
    analyze_existing_graph
)

from comparison import (
    edge_jaccard_table,
    hub_overlap_table,
    edge_sign_table,
)

from spiec import (
    load_spiec_network,
)


DEBUG = False

DATASET = "HMP"

RESULTS_DIR = Path("results") / DATASET

PIPELINES = [
    ("relative", "spearman"),
    ("relative", "pearson"),
    ("clr", "spearman"),
    ("clr", "pearson"),
]


def save_results(results):
    """
    Save every network's outputs.
    """

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    for name, result in results.items():

        result["edges"].to_csv(
            RESULTS_DIR / f"{name}_edges.csv",
            index=False,
        )

        pd.DataFrame([result["summary"]]).to_csv(
            RESULTS_DIR / f"{name}_summary.csv",
            index=False,
        )

        nx.write_graphml(
            result["graph"],
            RESULTS_DIR / f"{name}.graphml",
        )

        centrality = result["centrality"]

        centrality.to_csv(
            RESULTS_DIR / f"{name}_centrality.csv",
            index=False,
        )

        result["degrees"].to_csv(
            RESULTS_DIR /f"{name}_degrees.csv",
            index=False
        )


def main():

    abundance, metadata = load_data(
        f"data/{DATASET}/abundance.csv",
        f"data/{DATASET}/metadata.csv",
    )

    filtered = prevalence_filter(
        abundance,
        min_prevalence=0.10,
    )

    filtered.to_csv(
        "results/filtered_abundance.csv"
    )

    results = {}

    # -----------------------------
    # Run correlation pipelines
    # -----------------------------

    for transform, association in PIPELINES:

        key = f"{transform}_{association}"

        results[key] = run_pipeline(
            abundance,
            transform=transform,
            association=association,
            prevalence=0.10,
    )
    # -----------------------------
    # Load SPIEC-EASI network
    # -----------------------------

    G_spiec = load_spiec_network(
        RESULTS_DIR / "spiec_easi_edges.csv"
    )

    results["spiec"] = analyze_existing_graph(
        G_spiec,
        method="spiec_easi",
        edges_path=RESULTS_DIR / "spiec_easi_edges.csv",
    )

    # -----------------------------
    # Save everything
    # -----------------------------

    save_results(results)

    # -----------------------------
    # Jaccard comparison
    # -----------------------------

    jaccard = edge_jaccard_table(results)

    jaccard.to_csv(
        RESULTS_DIR / "edge_jaccard.csv"
    )

    hub_overlap_10 = hub_overlap_table(results, top_n=10, metric="Betweenness")
    hub_overlap_20 = hub_overlap_table(results, top_n=20, metric="Betweenness")
    hub_overlap_50 = hub_overlap_table(results, top_n=50, metric="Betweenness")

    hub_overlap_10.to_csv(
        RESULTS_DIR / "hub_overlap_top10.csv"
    )
    hub_overlap_20.to_csv(
            RESULTS_DIR / "hub_overlap_top20.csv"
        )   
        
    hub_overlap_50.to_csv(
        RESULTS_DIR / "hub_overlap_top50.csv"
    )

    edge_signs = edge_sign_table(results)

    edge_signs.to_csv(
        RESULTS_DIR / "edge_sign_summary.csv",
        index=False,
    )

if __name__ == "__main__":
    main()