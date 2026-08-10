import pandas as pd


def network_summary_table(results):
    """
    Combine the network summary statistics from all methods.

    Parameters
    ----------
    results : dict
        Dictionary of pipeline results.

    Returns
    -------
    pandas.DataFrame
        One row per inference method.
    """

    summaries = []

    for result in results.values():
        summaries.append(result["summary"])

    return pd.DataFrame(summaries)


def edge_jaccard_table(results):
    """
    Compute pairwise Jaccard similarity of edge sets.

    Parameters
    ----------
    results : dict
        Dictionary of pipeline results.

    Returns
    -------
    pandas.DataFrame
        Pairwise Jaccard similarity matrix.
    """

    methods = list(results.keys())

    edge_sets = {}

    for method in methods:

        edges = results[method]["edges"]

        # Correlation methods: keep only significant edges
        if "significant" in edges.columns:
            edges = edges.loc[edges["significant"]]

        edge_sets[method] = {
            frozenset((row["taxon1"], row["taxon2"]))
            for _, row in edges.iterrows()
        }

    table = pd.DataFrame(
        index=methods,
        columns=methods,
        dtype=float,
    )

    for m1 in methods:
        for m2 in methods:

            intersection = len(
                edge_sets[m1] & edge_sets[m2]
            )

            union = len(
                edge_sets[m1] | edge_sets[m2]
            )

            if union == 0:
                value = 0.0
            else:
                value = intersection / union

            table.loc[m1, m2] = value

    return table


def hub_overlap_table(
    results,
    top_n=20,
    metric="Degree",
):
    """
    Compare overlap of the highest-centrality taxa.

    Parameters
    ----------
    results : dict
        Dictionary of pipeline results.

    top_n : int
        Number of top taxa to compare.

    metric : str
        Centrality column used for ranking.

    Returns
    -------
    pandas.DataFrame
        Pairwise overlap fractions.
    """

    methods = list(results.keys())

    hub_sets = {}

    for method in methods:

        centrality = (
            results[method]["centrality"]
            .sort_values(metric, ascending=False)
        )

        hub_sets[method] = set(
            centrality.head(top_n)["Taxon"]
        )

    table = pd.DataFrame(
        index=methods,
        columns=methods,
        dtype=float,
    )

    for m1 in methods:
        for m2 in methods:

            overlap = len(
                hub_sets[m1] & hub_sets[m2]
            )

            table.loc[m1, m2] = overlap / top_n

    return table


def edge_sign_table(results):
    """
    Count positive and negative edges.

    SPIEC-EASI is omitted because the current
    implementation produces unsigned edges.

    Parameters
    ----------
    results : dict

    Returns
    -------
    pandas.DataFrame
    """

    rows = []

    for method, result in results.items():

        if method == "spiec":
            rows.append({
                "Method": method,
                "PositiveEdges": None,
                "NegativeEdges": None,
                "PercentPositive": None,
            })
            continue

        graph = result["graph"]

        n_positive = 0
        n_negative = 0

        for _, _, data in graph.edges(data=True):

            if data["weight"] > 0:
                n_positive += 1

            elif data["weight"] < 0:
                n_negative += 1

        total = n_positive + n_negative

        rows.append({
            "Method": method,
            "PositiveEdges": n_positive,
            "NegativeEdges": n_negative,
            "PercentPositive": (
                n_positive / total
                if total > 0
                else None
            ),
        })

    return pd.DataFrame(rows)