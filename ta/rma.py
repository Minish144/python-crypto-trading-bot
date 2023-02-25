def rma(df, window):
    """
    Calculates the Recursive Moving Average (RMA) indicator for a given window.

    Args:
    df (pandas.DataFrame): The input DataFrame.
    window (int): The number of periods to use in the RMA calculation.

    Returns:
    pandas.DataFrame: A new DataFrame with the RMA indicator values.
    """
    rma = df['close'].rolling(window=window).mean()

    alpha = 1 / window

    for i in range(window, len(df)):
        rma[i] = alpha * df['close'].iloc[i] + (1 - alpha) * rma.iloc[i-1]

    return rma
