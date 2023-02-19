from re import I

from blankly import Binance, Strategy

from strategies.grid import Grid
from strategies.ichimoku import Ichimoku
from strategies.macd import MACD
from strategies.rsi import RSI

exchange = Binance()
s = Strategy(exchange)

s.add_price_event(Grid.price_event, 'BTC-USDT', '1m', Grid.init(3600, 0.1, 0.05, 3))
s.backtest('2M', {'USDT': 100000, 'BTC': 4})
