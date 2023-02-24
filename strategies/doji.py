from blankly import StrategyState
from blankly.utils import count_decimals, trunc

DAYS = 3
TRADE_SIZE = 0.001
MAX_ORDER_USDT = 95

class Doji:
    @staticmethod
    def init(symbol, state: StrategyState):
        order_filters = state.interface.get_order_filter(symbol)['limit_order']

        state.variables["price_decimals"] = count_decimals(order_filters['price_increment'])
        state.variables["qty_decimals"]   = count_decimals(order_filters['base_increment'])
        state.variables['own_position']   = False

    @staticmethod
    def price_event(price, symbol, state: StrategyState):
        kandles = state.interface.history(symbol=symbol, to=DAYS-1, resolution=state.resolution, return_as='df')

        if len(kandles) < DAYS:
            return

        if pure_morning(kandles):
            if not state.variables['own_position']:
                # If the pattern is found and we're not already in a position, enter a long position
                state.interface.market_order(
                    symbol,
                    'buy',
                    get_buy_order_qty(price, state),
                )
                state.variables['own_position'] = True
        else:
            if state.variables['own_position']:
                # If the pattern is not found and we're in a position, exit the position
                print(state.interface.account[state.base_asset].available)
                state.interface.market_order(
                    symbol,
                    'sell',
                    state.interface.account[state.base_asset].available,
                )
                state.variables['own_position'] = False

def get_buy_order_qty(price: float, state: StrategyState):
    cash = state.interface.cash
    if cash > MAX_ORDER_USDT:
        cash = MAX_ORDER_USDT

    return trunc(cash / price * 0.95, state.variables['qty_decimals'])

# Pure Morning pattern
def pure_morning(df):
    # Check for a bullish engulfing pattern on day 1
    if (
        df.iloc[0]["open"] > df.iloc[0]["close"] and
        df.iloc[1]["open"] < df.iloc[1]["close"] and
        df.iloc[1]["open"] > df.iloc[0]["close"] and
        df.iloc[1]["close"] > df.iloc[0]["open"] and
        df.iloc[1]["high"] > df.iloc[0]["high"]
    ):
        # Check for a doji on day 2
        if (
            abs(df.iloc[2]["open"] - df.iloc[2]["close"]) < 0.01 * df.iloc[2]["open"]
        ):
            return True

    return False

