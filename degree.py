import pandas as pd

def degree_distribution(G):
    """
    Return the degree of every node.
    """

    degrees = dict(G.degree())

    df = pd.DataFrame({
        "Taxon": list(degrees.keys()),
        "Degree": list(degrees.values())
    })

    return df.sort_values(
        "Degree",
        ascending=False
    )