def rsi(df, window):
    """
    Calculates the Relative Strength Index (RSI) indicator for a given window.

    Args:
    df (pandas.DataFrame): The input DataFrame.
    window (int): The number of periods to use in the RSI calculation.

    Returns:
    pandas.DataFrame: A new DataFrame with the RSI indicator values.
    """
    delta = df['close'].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=window-1, adjust=False).mean()
    ema_down = down.ewm(com=window-1, adjust=False).mean()
    rs = ema_up / ema_down
    rsi = 100 - (100 / (1 + rs))
    return rsi
