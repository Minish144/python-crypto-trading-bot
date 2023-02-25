import pandas as pd

def mfi(df, n):
    """
    Calculates the Money Flow Index (MFI) indicator for a given window (n).

    Args:
    df (pandas.DataFrame): The input DataFrame.
    n (int): The number of periods to use in the MFI calculation.

    Returns:
    pandas.DataFrame: A new DataFrame with the MFI indicator values.
    """
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    money_flow = typical_price * df['volume']
    positive_flow = []
    negative_flow = []

    for i in range(1, len(typical_price)):
        if typical_price.iloc[i] > typical_price.iloc[i-1]:
            positive_flow.append(money_flow.iloc[i-1])
            negative_flow.append(0)
        elif typical_price.iloc[i] < typical_price.iloc[i-1]:
            positive_flow.append(0)
            negative_flow.append(money_flow.iloc[i-1])
        else:
            positive_flow.append(0)
            negative_flow.append(0)

    positive_flow = pd.Series(positive_flow, index=df.index[1:])
    negative_flow = pd.Series(negative_flow, index=df.index[1:])

    mfi_ratio = 100 - (100 / (1 + (positive_flow.rolling(n).sum() / negative_flow.rolling(n).sum())))

    return mfi_ratio
