from blankly import FuturesStrategyState, Side
import blankly
from blankly.enums import MarginType
from blankly.futures.utils import close_position

LEVERAGE = 3
ORDER_SIZE = 0.03

class RSIFutures:
    @staticmethod
    def init(symbol, state: FuturesStrategyState):
        state.interface.set_margin_type(symbol, MarginType.CROSSED)
        state.interface.set_leverage(LEVERAGE, symbol)
        close_position(symbol, state)

        state.variables['history'] = state.interface.history(symbol, resolution=state.resolution, return_as='deque')['close']

    @staticmethod
    def price_event(price, symbol, state: FuturesStrategyState):
        state.variables['history'].append(price)

        rsi = blankly.indicators.rsi(state.variables['history'])

        position = state.interface.get_position(symbol)
        position_size = position['size'] if position else 0

        if rsi[-1] < 35:
            side = Side.BUY
        elif rsi[-1] > 75:
            side = Side.SELL
        else:
            close_position(symbol, state)
            return

        if (position_size != 0) and (side == Side.BUY) == (position_size > 0):
            return

        # order_size = (state.interface.cash / price) * 0.99
        #
        # if order_size <= 0:
        #     return

        state.interface.market_order(symbol, side=side, size=ORDER_SIZE)
