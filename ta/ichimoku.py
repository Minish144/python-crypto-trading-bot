import pandas as pd

def ichimoku(df):
    # Calculate Tenkan-sen (Conversion Line)
    period9_high = df['high'].rolling(window=9).max()
    period9_low = df['low'].rolling(window=9).min()
    tenkan_sen = (period9_high + period9_low) / 2

    # Calculate Kijun-sen (Base Line)
    period26_high = df['high'].rolling(window=26).max()
    period26_low = df['low'].rolling(window=26).min()
    kijun_sen = (period26_high + period26_low) / 2

    # Calculate Senkou Span A (Leading Span A)
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)

    # Calculate Senkou Span B (Leading Span B)
    period52_high = df['high'].rolling(window=52).max()
    period52_low = df['low'].rolling(window=52).min()
    senkou_span_b = ((period52_high + period52_low) / 2).shift(26)

    # Calculate Chikou Span (Lagging Span)
    chikou_span = df['close'].shift(-26)

    # Combine all components into a single DataFrame
    ichimoku_df = pd.concat([tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span], axis=1)
    ichimoku_df.columns = ['tenkan_sen', 'kijun_sen', 'senkou_span_a', 'senkou_span_b', 'chikou_span']

    return ichimoku_df.iloc[-1]
