from blankly import Binance, BinanceFutures, Strategy

from strategies.grid import Grid
from strategies.ichimoku import Ichimoku
from strategies.macd import MACD
from strategies.rsi import RSI
from strategies.rsifutures import RSIFutures

exchange = BinanceFutures()
s = Strategy(exchange)

# s.add_price_event(Grid.price_event, 'BTC-USDT', '1m', Grid.init(3600, 0.1, 0.05, 3))
s.add_price_event(RSIFutures.price_event, 'ETH-USDT', '1h', RSIFutures.init)
s.start()
