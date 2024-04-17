import plotly.express as px

import polars as pl

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

def proportion_plot(
        data , column,target,title
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