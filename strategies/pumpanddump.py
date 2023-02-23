import blankly
from blankly import StrategyState
import pandas as pd

VOL_MEAN_THRESHOLD = 3
PRICE_MEAN_THRESHOLD = 1.005
PRICE_MEAN_MAX_THRESHOLD = 1.07
TAKE_PROFIT_COEFF = 1.15
STOP_LOSS_COEFF = 0.96

class PumpAndDump:
    @staticmethod
    def init(symbol, state: StrategyState):
        state.variables['kandles'] = pd.DataFrame(state.interface.history(symbol, resolution=state.resolution, to=86400, return_as='df'))
        state.variables['own_position']      = False
        state.variables['position_price']    = 0
        state.variables['take_profit_price'] = 0

    @staticmethod
    def price_event(price, symbol, state: StrategyState):
        last_kandle = state.interface.history(symbol, resolution=state.resolution, to=0, return_as='df')
        kandles = pd.concat((state.variables['kandles'].iloc[1:], last_kandle))
        state.variables['kandles'] = kandles

        kandles_except_last: pd.DataFrame = kandles.iloc[:-1]
        last_kandle: pd.Series            = kandles.iloc[-1]

        volume_avg     = kandles_except_last['volume'].median()
        current_volume = last_kandle['volume']

        price_avg = kandles_except_last['close'].median()

        # BUY BEFORE PUMP
        if not state.variables['own_position']:
            if current_volume >= VOL_MEAN_THRESHOLD * volume_avg \
                and price >= PRICE_MEAN_THRESHOLD * price_avg \
                and price < PRICE_MEAN_MAX_THRESHOLD * price_avg:
                qty = blankly.trunc(state.interface.cash / price * 0.9, 4)

                state.interface.market_order(symbol, 'buy', qty)

                state.variables['position_price'] = price
                state.variables['own_position']   = True

                state.variables['take_profit_price'] = blankly.trunc(TAKE_PROFIT_COEFF * price, 7)

                print('\nBUY!', "volume", current_volume, "avg_volume", volume_avg, "price", price, "qty", qty)

                return

        # SELL ON DUMP
        if state.variables['own_position']:
            price_max = state.variables['kandles']['high'].max()

            if state.variables['position_price'] * 1.25 >= price and price <= price_max * 0.9:
                qty = state.interface.account[state.base_asset].available

                state.interface.market_order(symbol, 'sell', qty)

                print("\nSELL ON DUMP!", "price", price, "qty", qty)

                state.variables['position_price'] = 0
                state.variables['own_position'] = False

                return


        # STOP LOSS
        if state.variables['own_position'] and price <= STOP_LOSS_COEFF * state.variables['position_price']:
            for o in state.interface.get_open_orders(symbol):
                state.interface.cancel_order(symbol, o.get_order_id())

            qty = state.interface.account[state.base_asset].available

            state.interface.market_order(symbol, 'sell', qty)

            print("\nSTOP LOSS!", "price", price, "qty", qty)

            state.variables['position_price'] = 0
            state.variables['own_position'] = False

            return

        # TAKE PROFIT
        if state.variables['own_position'] and len(state.interface.get_open_orders(symbol)) == 0:
            qty = state.interface.account[state.base_asset].available
            tp_price = state.variables['take_profit_price']

            if price >= tp_price:
                state.interface.market_order(symbol, 'sell', qty)
                state.variables['own_position'] = False

                print("\nTAKE PROFIT!", "price", price, "qty", qty)

                return
