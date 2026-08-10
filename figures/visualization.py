from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import networkx as nx

RESULTS_DIR = Path("results/HMP")
FIGURES_DIR = Path("figures")

FIGURES_DIR.mkdir(exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

METHOD_COLORS = {
    "Relative\nSpearman": "#4E79A7",
    "Relative\nPearson": "#F28E2B",
    "CLR\nSpearman": "#59A14F",
    "CLR\nPearson": "#E15759",
    "SPIEC-EASI": "#B07AA1",
}


def load_summaries():

    summaries = []

    for file in RESULTS_DIR.glob("*_summary.csv"):

        df = pd.read_csv(file)
        summaries.append(df)
    summary = pd.concat(summaries, ignore_index=True)

    valid_methods = [
        "relative_spearman",
        "relative_pearson",
        "clr_spearman",
        "clr_pearson",
        "spiec_easi",
    ]

    summary = summary[summary["Method"].isin(valid_methods)].copy()

    label_map = {
        "relative_spearman": "Relative\nSpearman",
        "relative_pearson": "Relative\nPearson",
        "clr_spearman": "CLR\nSpearman",
        "clr_pearson": "CLR\nPearson",
        "spiec_easi": "SPIEC-EASI",
    }

    method_order = [
        "relative_spearman",
        "relative_pearson",
        "clr_spearman",
        "clr_pearson",
        "spiec_easi",
    ]

    summary["Method"] = pd.Categorical(
        summary["Method"],
        categories=method_order,
        ordered=True,
    )

    summary = summary.sort_values("Method")

    summary["Method"] = summary["Method"].replace(label_map)

    return summary

def network_summary_figure():
    summary = load_summaries()

    metrics = [
        "Edges",
        "Density",
        "Average Degree",
        "Average Clustering",
    ]

    label_map = {
    "relative_spearman":"Relative\nSpearman",
    "relative_pearson":"Relative\nPearson",
    "clr_spearman":"CLR\nSpearman",
    "clr_pearson":"CLR\nPearson",
    "spiec_easi":"SPIEC-EASI",
    }

    summary["Method"] = summary["Method"].replace(label_map)

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(12, 8)
    )

    axes = axes.flatten()

    for ax, metric in zip(axes, metrics):

        colors = [METHOD_COLORS[m] for m in summary["Method"]]

        ax.bar(
            summary["Method"],
            summary[metric],
            color=colors,
        )

        ax.set_title(metric)

        ax.tick_params(
            axis="x",
            rotation=20
        )

    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / "network_summary.png",
        dpi=300,
    )

    plt.close()


def edge_jaccard_heatmap():

    jaccard = pd.read_csv(
        RESULTS_DIR / "edge_jaccard.csv",
        index_col=0,
    )

    label_map = {
        "relative_spearman": "Relative\nSpearman",
        "relative_pearson": "Relative\nPearson",
        "clr_spearman": "CLR\nSpearman",
        "clr_pearson": "CLR\nPearson",
        "spiec_easi": "SPIEC-EASI",
    }

    jaccard.rename(
        index=label_map,
        columns=label_map,
        inplace=True,
    )

    fig, ax = plt.subplots(figsize=(7, 6))

    im = ax.imshow(
        jaccard,
        vmin=0,
        vmax=1,
        cmap="viridis",
    )

    ax.set_xticks(np.arange(len(jaccard.columns)))
    ax.set_yticks(np.arange(len(jaccard.index)))

    ax.set_xticklabels(jaccard.columns)
    ax.set_yticklabels(jaccard.index)

    plt.setp(
        ax.get_xticklabels(),
        rotation=35,
        ha="right",
    )

    for i in range(jaccard.shape[0]):
        for j in range(jaccard.shape[1]):

            value = jaccard.iloc[i, j]

            ax.text(
                j,
                i,
                f"{value:.2f}",
                ha="center",
                va="center",
                color="white" if value < 0.50 else "black",
                fontsize=10,
            )

    cbar = fig.colorbar(im)
    cbar.set_label("Edge Jaccard Similarity")

    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / "edge_jaccard_heatmap.png",
        dpi=300,
    )

    plt.close()

def hub_overlap_heatmap(top_n=20):

    overlap = pd.read_csv(
        RESULTS_DIR / f"hub_overlap_top{top_n}.csv",
        index_col=0,
    )

    label_map = {
        "relative_spearman": "Relative\nSpearman",
        "relative_pearson": "Relative\nPearson",
        "clr_spearman": "CLR\nSpearman",
        "clr_pearson": "CLR\nPearson",
        "spiec_easi": "SPIEC-EASI",
    }

    overlap.rename(
        index=label_map,
        columns=label_map,
        inplace=True,
    )

    fig, ax = plt.subplots(figsize=(7,6))

    im = ax.imshow(
        overlap,
        vmin=0,
        vmax=1,
        cmap="viridis",
    )

    ax.set_xticks(np.arange(len(overlap.columns)))
    ax.set_yticks(np.arange(len(overlap.index)))

    ax.set_xticklabels(overlap.columns)
    ax.set_yticklabels(overlap.index)

    plt.setp(
        ax.get_xticklabels(),
        rotation=35,
        ha="right",
    )

    for i in range(overlap.shape[0]):
        for j in range(overlap.shape[1]):

            value = overlap.iloc[i, j]

            ax.text(
                j,
                i,
                f"{value:.2f}",
                ha="center",
                va="center",
                color="white" if value < 0.50 else "black",
                fontsize=10,
            )

    cbar = fig.colorbar(im)
    cbar.set_label(f"Top-{top_n} Hub Overlap")

    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / f"hub_overlap_{top_n}.png",
        dpi=300,
    )

    plt.close()

def edge_sign_figure():

    signs = pd.read_csv(
        RESULTS_DIR / "edge_sign_summary.csv"
    )

    # SPIEC-EASI has unsigned edges
    signs = signs.dropna()

    label_map = {
        "relative_spearman": "Relative\nSpearman",
        "relative_pearson": "Relative\nPearson",
        "clr_spearman": "CLR\nSpearman",
        "clr_pearson": "CLR\nPearson",
    }

    signs["Method"] = signs["Method"].replace(label_map)

    # Convert to percentages
    total = signs["PositiveEdges"] + signs["NegativeEdges"]

    signs["PositivePercent"] = (
        100 * signs["PositiveEdges"] / total
    )

    signs["NegativePercent"] = (
        100 * signs["NegativeEdges"] / total
    )

    fig, ax = plt.subplots(figsize=(8,5))

    ax.bar(
        signs["Method"],
        signs["PositivePercent"],
        label="Positive",
        color="steelblue"
    )

    ax.bar(
        signs["Method"],
        signs["NegativePercent"],
        bottom=signs["PositivePercent"],
        label="Negative",
        color="indianred"
    )

    for i, row in signs.iterrows():

        ax.text(
            i,
            row["PositivePercent"] / 2,
            f'{row["PositivePercent"]:.1f}%',
            ha="center",
            va="center",
            fontsize=9,
        )

        ax.text(
            i,
            row["PositivePercent"] + row["NegativePercent"] / 2,
            f'{row["NegativePercent"]:.1f}%',
            ha="center",
            va="center",
            fontsize=9,
        )
    ax.set_ylim(0,100)

    ax.set_ylabel("Percentage of edges")

    ax.set_title("Positive and Negative Associations")

    ax.legend()

    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / "edge_signs.png",
        dpi=300,
    )

    plt.close()

def degree_distribution_figure():
    fig, ax = plt.subplots(figsize=(7, 5))

    graphs = {
    "Relative\nSpearman":"relative_spearman.graphml",
    "Relative\nPearson":"relative_pearson.graphml",
    "CLR\nSpearman":"clr_spearman.graphml",
    "CLR\nPearson":"clr_pearson.graphml",
    "SPIEC-EASI":"spiec.graphml",
    }

    for label, filename in graphs.items():

        G = nx.read_graphml(
            RESULTS_DIR / filename
        )

        degrees = sorted(
            [d for _, d in G.degree()]
        )

        degrees = np.array(degrees)

        x = np.unique(degrees)

        y = [
            np.mean(degrees >= k)
            for k in x
        ]

        ax.plot(
        x,
        y,
        marker=None,
        linewidth=2,
        markersize=4,
        label=label,
        )

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_xlabel("Degree")

    ax.set_ylabel("P(K ≥ k)")

    ax.set_title("Degree distributions")

    ax.legend(
    bbox_to_anchor=(1.02,1),
    loc="upper left",
    )

    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR/"degree_distribution.png",
        dpi=300,
    )

    plt.close()


def network_visualization():

    fig, axes = plt.subplots(
        2,
        3,
        figsize=(15, 10)
    )

    graphs = {
        "Relative Spearman":"relative_spearman.graphml",
        "Relative Pearson":"relative_pearson.graphml",
        "CLR Spearman":"clr_spearman.graphml",
        "CLR Pearson":"clr_pearson.graphml",
        "SPIEC-EASI":"spiec.graphml",
    }

    axes = axes.flatten()

    for ax, (title, filename) in zip(axes, graphs.items()):

        G = nx.read_graphml(
            RESULTS_DIR / filename
        )

        pos = nx.spring_layout(
            G,
            seed=42,
            k=0.2,
        )

        degree = dict(G.degree())

        centrality = nx.degree_centrality(G)

        node_sizes = [
            10 + degree[node] * 3
            for node in G.nodes()
        ]

        node_colors = [
            centrality[node]
            for node in G.nodes()
        ]

        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax,
            edge_color="lightgray",
            alpha=0.18,
            width=0.5,
        )

        cmap = "viridis"
        nx.draw_networkx_nodes(
            G,
            pos,
            ax=ax,
            node_size=node_sizes,
            node_color=node_colors,
            cmap=cmap,
            linewidths=0,
        )

        ax.set_title(title)
        ax.axis("off")

    axes[-1].axis("off")

    sm = plt.cm.ScalarMappable(
        cmap=cmap,
        norm=plt.Normalize(
            vmin=0,
            vmax=max(node_colors),
        ),
    )

    sm.set_array([])

    cbar = fig.colorbar(
        sm,
        ax=axes,
        fraction=0.03,
        pad=0.02,
    )

    cbar.set_label("Degree Centrality")

    plt.subplots_adjust(
        wspace=0.15,
        hspace=0.15,
        right=0.88,
    )

    plt.savefig(
        FIGURES_DIR /
        "network_visualization.png",
        dpi=300,
    )

    plt.close()

if __name__ == "__main__":

    network_summary_figure()

    edge_jaccard_heatmap()

    hub_overlap_heatmap()

    edge_sign_figure()

    degree_distribution_figure()

    network_visualization()