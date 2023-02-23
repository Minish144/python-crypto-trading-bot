from blankly import Binance, BinanceFutures, Kucoin, Strategy

from strategies.grid import Grid
from strategies.ichimoku import Ichimoku
from strategies.macd import MACD
from strategies.pumpanddump import PumpAndDump
from strategies.rsi import RSI
from strategies.rsifutures import RSIFutures

exchange = Kucoin()
s = Strategy(exchange)

# s.add_price_event(Grid.price_event, 'BTC-USDT', '1m', Grid.init(3600, 0.1, 0.05, 3))
s.add_price_event(PumpAndDump.price_event, 'SON-USDT', '1h', PumpAndDump.init)
# s.add_price_event(PumpAndDump.price_event, 'AMP-USDT', '30m', PumpAndDump.init)
# s.backtest(initial_values={'RIF': 900, 'USDT': 100}, start_date=1673312400, end_date=1673398800)
s.backtest('1M', {'USDT': 100})
