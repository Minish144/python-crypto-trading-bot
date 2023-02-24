import blankly
from blankly import StrategyState
from blankly.utils import count_decimals, time_interval_to_seconds

VOL_MEAN_THRESHOLD = 10
PRICE_MEAN_THRESHOLD = 1.005
PRICE_MEAN_MAX_THRESHOLD = 1.3
TAKE_PROFIT_COEFF = 1.3
STOP_LOSS_COEFF = 0.92
POSITION_TIMEOUT = time_interval_to_seconds('3d')

MAX_ORDER_USDT = 98

class PumpAndDump:
    @staticmethod
    def init(symbol, state: StrategyState):
        order_filters = state.interface.get_order_filter(symbol)['limit_order']

        state.variables["price_decimals"]    = count_decimals(order_filters['price_increment'])
        state.variables["qty_decimals"]      = count_decimals(order_filters['base_increment'])
        state.variables["position_price"]    = 0
        state.variables["take_profit_price"] = 0
        state.variables["position_time"]     = 0
        state.variables["own_position"]      = False

    @staticmethod
    def price_event(price, symbol, state: StrategyState):
        kandles = state.interface.history(symbol, resolution=state.resolution, return_as="df")
        if len(kandles) == 0:
            return

        state.variables["kandles"] = kandles

        kandles_except_last = kandles.iloc[:-1]
        last_kandle         = kandles.iloc[-1]
        volume_avg          = kandles_except_last["volume"].median()
        current_volume      = last_kandle["volume"]
        price_avg           = kandles_except_last["close"].median()

        # BUY BEFORE PUMP
        if not state.variables["own_position"]:
            if current_volume >= VOL_MEAN_THRESHOLD * volume_avg and \
               price >= PRICE_MEAN_THRESHOLD * price_avg and \
               price < PRICE_MEAN_MAX_THRESHOLD * price_avg:
                qty = get_buy_order_qty(price, state)

                state.interface.market_order(symbol, "buy", qty)

                state.variables["position_price"]    = price
                state.variables["position_time"]     = state.time
                state.variables["own_position"]      = True
                state.variables["take_profit_price"] = blankly.trunc(TAKE_PROFIT_COEFF * price, state.variables['price_decimals'])

                print("\nBUY!", "volume", current_volume, "avg_volume", volume_avg, "price", price, "qty", qty)

                return

        # SELL ON DUMP
        if state.variables["own_position"]:
            price_max = kandles_except_last["close"].max()

            if state.variables["position_price"] * 1.25 >= price and price <= price_max * 0.9:
                qty = state.interface.account[state.base_asset].available

                state.interface.market_order(symbol, "sell", qty)

                state.variables["position_price"]    = 0
                state.variables["position_time"]     = 0
                state.variables["take_profit_price"] = 0
                state.variables["own_position"]      = False

                print("\nSELL ON DUMP!", "price", price, "qty", qty)

                return

        # STOP LOSS or TIMEOUT
        if state.variables["own_position"]:
            if price <= STOP_LOSS_COEFF * state.variables["position_price"] or \
               state.time >= state.variables["position_time"] + POSITION_TIMEOUT:
                for o in state.interface.get_open_orders(symbol):
                    state.interface.cancel_order(symbol, o.get_order_id())

                qty = state.interface.account[state.base_asset].available

                state.interface.market_order(symbol, "sell", qty)

                state.variables["position_price"]    = 0
                state.variables["position_time"]     = 0
                state.variables["take_profit_price"] = 0
                state.variables["own_position"]      = False

                print("\nSTOP LOSS!", "price", price, "qty", qty)

                return

        # TAKE PROFIT
        if state.variables["own_position"] and len(state.interface.get_open_orders(symbol)) == 0:
            qty = state.interface.account[state.base_asset].available
            tp_price = state.variables["take_profit_price"]

            if price >= tp_price:
                state.interface.market_order(symbol, "sell", qty)

                state.variables["position_price"]    = 0
                state.variables["position_time"]     = 0
                state.variables["take_profit_price"] = 0
                state.variables["own_position"]      = False

                print("\nTAKE PROFIT!", "price", price, "qty", qty)

                return

def get_buy_order_qty(price: float, state: StrategyState):
    cash = state.interface.cash
    if cash > MAX_ORDER_USDT:
        cash = MAX_ORDER_USDT

    return blankly.trunc(cash / price * 0.95, state.variables['qty_decimals'])
