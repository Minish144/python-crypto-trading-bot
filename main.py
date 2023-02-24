from time import sleep

from blankly import Binance, BinanceFutures, Kucoin, Strategy

from strategies.doji import Doji
from strategies.grid import Grid
from strategies.ichimoku import Ichimoku
from strategies.macd import MACD
from strategies.pumpanddump import PumpAndDump
from strategies.rsi import RSI
from strategies.rsifutures import RSIFutures

# exchange = Kucoin()
exchange = Binance()
s = Strategy(exchange)

kucoin_symbols = [
    'HBB-USDT',
    'ILA-USDT',
    'SPA-USDT',
    'STND-USDT',
    'EOSC-USDT',
]

binance_symbols = [
    'BTC-USDT',
    'ETH-USDT',
]

symbols = binance_symbols

for symbol in symbols:
    s.add_price_event(Doji.price_event, symbol, '1d', Doji.init)
    print("Added", symbol)

s.backtest(initial_values={'USDT': 100 * len(symbols)}, to='1y')
# s.backtest(initial_values={'USDT': 100 * len(symbols)}, start_date=1661620392, end_date=1677172392)
