from time import sleep

from blankly import Binance, BinanceFutures, Kucoin, Strategy

from strategies.doji import Doji
from strategies.grid import Grid
from strategies.ichimoku import Ichimoku
from strategies.macd import MACD
from strategies.pumpanddump import PumpAndDump
from strategies.puremorning import PureMorning
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
    'DASH-USDT'
]

symbols = binance_symbols

for symbol in symbols:
    s.add_price_event(PureMorning.price_event, symbol, '4h', PureMorning.init)
    print("Added", symbol)

s.backtest(initial_values={'USDT': 100 * len(symbols)}, to='3M')
