import pandas as pd
from warnings import warn


def read_checkm_output(taxonomy_table, completness_table):

    c_df = pd.read_csv(completness_table, index_col=0, sep="\t")[
        ["Completeness", "Contamination", "Strain heterogeneity"]
    ]
    t_df = pd.read_csv(taxonomy_table, index_col=0, sep="\t")[
        [
            "# unique markers (of 43)",
            "# multi-copy",
            "Insertion branch UID",
            "Taxonomy (contained)",
            "Taxonomy (sister lineage)",
            "GC",
            "Genome size (Mbp)",
            "Gene count",
            "Coding density",
        ]
    ]
    df = pd.concat([c_df, t_df], axis=1)
    return df


def load_quality(quality_file):
    Q = pd.read_csv(quality_file, index_col=0, sep="\t")

    # remove extension if present
    if Q.index.str.contains(".fa").all():
        warn("Found fasta extension in index. I remove them")
        Q.index = Q.index.str.split(".fa", expand=True).to_frame()[0]

    Q.columns = Q.columns.str.lower()

    necessary_columns = ["Completeness", "Contamination"]

    # rename lower and uppercase to necessary_columns
    Q = Q.rename(
        columns={fun(s): s for s in necessary_columns for fun in (str.lower, str.upper)}
    )

    if Q.columns.isin(necessary_columns).sum() != len(necessary_columns):
        raise Exception(
            f"{necessary_columns} should be in the quality table, only got {Q.columns}"
        )

    assert not Q.index.duplicated().any(), f"duplicated indexes in {quality_file}"

    return Q
