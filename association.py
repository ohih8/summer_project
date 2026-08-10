import pandas as pd

from scipy.stats import spearmanr
from scipy.stats import pearsonr

from statsmodels.stats.multitest import multipletests


def pairwise_correlation(data, method="spearman"):
    """
    Compute pairwise correlations between all taxa.

    Parameters
    ----------
    data : pandas.DataFrame
        Taxa x samples abundance matrix.

    method : str
        "spearman" or "pearson"

    Returns
    -------
    pandas.DataFrame
        Edge table containing
        taxon1,
        taxon2,
        weight,
        pvalue,
        qvalue,
        significant
    """

    taxa = list(data.index)

    edges = []

    for i in range(len(taxa)):
        for j in range(i + 1, len(taxa)):

            x = data.loc[taxa[i]]
            y = data.loc[taxa[j]]

            if method == "spearman":
                rho, p = spearmanr(x, y)

            elif method == "pearson":
                rho, p = pearsonr(x, y)

            else:
                raise ValueError("Unknown correlation method.")

            edges.append(
                {
                    "taxon1": taxa[i],
                    "taxon2": taxa[j],
                    "weight": rho,
                    "pvalue": p,
                }
            )

    edges = pd.DataFrame(edges)

    reject, qvals, _, _ = multipletests(
        edges["pvalue"],
        method="fdr_bh",
    )

    edges["qvalue"] = qvals
    edges["significant"] = reject

    return edges