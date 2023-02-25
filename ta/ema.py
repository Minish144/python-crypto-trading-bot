def ema(df, window):
    """
    Calculates the Exponential Moving Average (EMA) indicator for a given window.

    Args:
    df (pandas.DataFrame): The input DataFrame.
    window (int): The number of periods to use in the EMA calculation.

    Returns:
    pandas.DataFrame: A new DataFrame with the EMA indicator values.
    """
    ema = df['close'].ewm(span=window, adjust=False).mean()
    return ema
