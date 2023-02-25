import numpy as np
import pandas as pd

def atr(df, window):
    """
    Calculates the Average True Range (ATR) indicator for a given window.

    Args:
    df (pandas.DataFrame): The input DataFrame.
    window (int): The number of periods to use in the ATR calculation.

    Returns:
    pandas.DataFrame: A new DataFrame with the ATR indicator values.
    """
    tr = pd.DataFrame(index=df.index, columns=['tr'])
    tr['tr'] = np.maximum(
        np.maximum(df['high'] - df['low'], np.abs(df['high'] - df['close'].shift(1))),
        np.abs(df['low'] - df['close'].shift(1)),
    )
    atr = tr.rolling(window=window).mean()
    return atr
