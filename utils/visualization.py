import plotly.express as px

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