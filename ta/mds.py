def mds(df, tolerance):
    range1 = df['high'].iloc[-3] - df['low'].iloc[-3]

    candle1 = abs(df['close'].iloc[-3] - df['open'].iloc[-3]) / range1 > 0.6 and df['close'].iloc[-3] < df['open'].iloc[-3]
    candle2 = ((df['open'].iloc[-2] > df['close'].iloc[-2] and df['open'].iloc[-2] < df['close'].iloc[-2] * (1 + tolerance)) or
               (df['open'].iloc[-2] < df['close'].iloc[-2] and df['open'].iloc[-2] > df['close'].iloc[-2] * (1 - tolerance))) and \
              df['close'].iloc[-2] < df['close'].iloc[-3] + range1
    candle3 = df['close'].iloc[-1] > df['open'].iloc[-1] and df['close'].iloc[-1] > (df['close'].iloc[-3] + range1)

    MDS = candle1 and candle2 and candle3

    return MDS
