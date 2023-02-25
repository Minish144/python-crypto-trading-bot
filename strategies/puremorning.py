from blankly import StrategyState
from blankly.utils import count_decimals, trunc

import ta

TOLERANCE       = 0.09  # MDS Tolerance
TOLERANCE1      = 0.05  # DOJI Tolerance

XL_SL_PERCENT   = 2     # Stop Loss
XL_TP_PERCENT   = 9     # Take Profit

MAX_ORDER_USDT = 990

class PureMorning:
    @staticmethod
    def init(symbol, state: StrategyState):
        order_filters                       = state.interface.get_order_filter(symbol)['limit_order']
        state.variables["price_decimals"]   = count_decimals(order_filters['price_increment'])
        state.variables["qty_decimals"]     = count_decimals(order_filters['base_increment'])
        state.variables["own_position"]     = False
        state.variables['xl_tp_price']      = 0
        state.variables['xl_sl_price']      = 0

    @staticmethod
    def price_event(price, symbol, state: StrategyState):
        kandles = state.interface.history(symbol=symbol, resolution=state.resolution, return_as='df')

        if len(kandles) <= 60:
            return

        close = kandles.iloc[-1]['close']

        # indicators
        ema60 = ta.ema(kandles, 60).iloc[-1]
        mds = ta.mds(kandles, TOLERANCE)
        doji = ta.doji(kandles, TOLERANCE1)

        # entry long
        el_cond    = doji and close > ema60
        el_cond_02 = mds and close > ema60

        if not state.variables['own_position']:
            if el_cond or el_cond_02:
                state.interface.market_order(
                    symbol,
                    'buy',
                    get_buy_order_qty(price, state),
                )
                state.variables['own_position'] = True

                # TP and SL
                state.variables['xl_tp_price'] = price * (1 + XL_TP_PERCENT / 100)
                state.variables['xl_sl_price'] = price * (1 - XL_SL_PERCENT / 100)

            return

        if state.variables['own_position'] and (price >= state.variables['xl_tp_price'] or price <= state.variables['xl_sl_price']):
            qty = state.interface.account[state.base_asset].available
            state.interface.market_order(symbol, "sell", qty)
            state.variables['own_position'] = False
            state.variables['xl_tp_price'] = 0
            state.variables['xl_sl_price'] = 0

            return

def get_buy_order_qty(price: float, state: StrategyState):
    cash = state.interface.cash
    if cash > MAX_ORDER_USDT:
        cash = MAX_ORDER_USDT

    print(
        cash / price * 0.98,
        trunc(cash / price * 0.98, state.variables['qty_decimals'])
    )

    return trunc(cash / price * 0.98, state.variables['qty_decimals'])


