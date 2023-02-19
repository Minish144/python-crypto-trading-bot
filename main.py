from re import I

from blankly import Binance, Strategy

from strategies.ichimoku import Ichimoku
from strategies.macd import MACD
from strategies.rsi import RSI

exchange = Binance()
s = Strategy(exchange)

s.add_price_event(Ichimoku.price_event, 'BTC-USDT', '1h', Ichimoku.init)
print(s.backtest('1y', {'USDT': 100000, 'BTC': 4}))
