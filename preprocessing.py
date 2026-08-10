import numpy as np
import pandas as pd


def load_data(abundance_path, metadata_path):
    """
    Load abundance and metadata tables.
    """

    abundance = pd.read_csv(
        abundance_path,
        index_col=0,
    )

    print(abundance.sum(axis=0).head())

    metadata = pd.read_csv(
        metadata_path,
        index_col=0,
    )

    return abundance, metadata



def prevalence_filter(
    abundance,
    min_prevalence=0.10,
):
    """
    Remove taxa present in fewer than
    min_prevalence fraction of samples.
    """

    prevalence = (abundance > 0).mean(axis=1)

    return abundance.loc[
        prevalence >= min_prevalence
    ]


def relative_abundance(abundance):

    totals = abundance.sum(axis=0)

    abundance = abundance.loc[:, totals > 0]

    totals = abundance.sum(axis=0)

    return abundance.div(
        totals,
        axis=1,
    )


def clr_transform(
    abundance,
    pseudocount=1e-6,
):
    """
    Centered log-ratio transformation.
    """

    abundance = abundance + pseudocount

    geometric_mean = np.exp(
        np.log(abundance).mean(axis=0)
    )

    clr = np.log(
        abundance.div(
            geometric_mean,
            axis=1,
        )
    )

    return clr