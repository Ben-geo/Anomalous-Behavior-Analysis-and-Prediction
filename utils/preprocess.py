import pyspark.sql.functions as F
from pyspark.sql.functions import isnan, when, count, col


def count_missings(df):
    """
    Args:
        df (pl.dataframe)
    Counts number of nulls and nans in each column
    """
    df.select([count(when(isnan(c), c)).alias(c) for c in df.columns]).show()
    df.select([count(when(isnan(c) | col(c).isNull(), c)).alias(c) for c in df.columns]).show()

