import plotly.express as px
import plotly.graph_objects as go
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

def bar_plot(data,column,title):
    """
    Args:
        data (pl.dataframe) 
        column (str)
        title (str)
    returns:
        px plot
    """
    count=data[column].value_counts(sort=True)
    fig = px.bar(
        x =count[column].to_list(),
        y =count["count"].to_list(),
        title = title,
        labels = {
            "x" : column,
            "y": "Count"
        }
        )
    return fig

def px_proportion_plot(
        data , column,target
) :
    """
    Args:
        data (pl.dataframe) :
        column (str) :
        target (str) :
        title (str) :
    returns:
        px plot
    """
    counts = data.groupby(column, target).agg(pl.count())
    target_counts = counts.groupby(column).agg(pl.col("count").sum().alias("total"))
    proportions = counts.join(target_counts, on=column)
    proportions = proportions.with_columns(
        proportion=pl.col("count") / pl.col("total")
    ).sort((column, target))
    title=columns +" vs "+ target
    fig = px.bar(
        x=proportions[column].to_list(),
        y=proportions["proportion"].to_list(),
        color=proportions[target].to_list(),
        color_discrete_sequence=px.colors.qualitative.Antique,
        labels={
            "x": column,
            "y": f"{target} proportion",
        },
        title=title,
    )
    return fig

def plt_proportion_plot(
        data , column,target
) :
    """
    Args:
        data (pl.dataframe) :
        column (str) :
        target (str) :
        title (str) :
    displays:
        plt plot
    """
    counts = data.groupby(column, target).agg(pl.count())
    target_counts = counts.groupby(column).agg(pl.col("count").sum().alias("total"))
    proportions = counts.join(target_counts, on=column)
    proportions = proportions.with_columns(
        proportion=pl.col("count") / pl.col("total")
    ).sort((column, target))
    sns.barplot(
        x=proportions[column].to_list(),
        y=proportions["proportion"].to_list(),
        hue=proportions[target],
    )
    plt.legend(title=target)
    plt.xlabel(column)
    plt.ylabel("Count")
    plt.title("Distribution of "+target+" based on "+column)
    plt.show()

def boxplot_by_bin_with_target(
    data: pl.DataFrame,
    column_to_bin: str,
    numeric_column: str,
    target: str,
    number_bins: int = 10,
) -> go.Figure:
    """Creates a plotly boxplot

    Args:
        data (pl.DataFrame): input dataframe
        column_to_bin (str): numeric column to bin
        numeric_column (str): numeric column to create a box plot from
        target (str): target column to colour a boxplot
        number_bins (int, optional): number of quantile bins to create. Defaults to 10.

    Returns:
        go.Figure: _description_
    """

    temp = data.select(
        pl.col(column_to_bin)
        .qcut(number_bins, allow_duplicates=True)
        .alias(f"{column_to_bin}_binned"),
        pl.col(column_to_bin),
        pl.col(numeric_column),
        pl.col(target),
    )

    order = (
        temp.groupby(f"{column_to_bin}_binned")
        .agg(pl.col(column_to_bin).min().alias("min"))
        .sort("min")[f"{column_to_bin}_binned"]
        .to_list()
    )

    fig = px.box(
        x=temp[f"{column_to_bin}_binned"].to_list(),
        y=temp[numeric_column].to_list(),
        color=temp[target].to_list(),
        color_discrete_sequence=px.colors.qualitative.Antique,
        log_y=True,
        category_orders={"x": order},
        labels={
            "x": "",
            "y": numeric_column,
        },
    )

    return fig