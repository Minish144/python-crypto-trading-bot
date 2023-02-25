def doji(df, tolerance):
    df = df.iloc[-1]

    is_oc_equal = (df['open'] > df['close'] and df['open'] < df['close'] * (1 + tolerance)) or \
                  (df['open'] < df['close'] and df['open'] > df['close'] * (1 - tolerance))

    return is_oc_equal
