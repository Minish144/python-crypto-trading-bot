from blankly import StrategyState

from ta.ichimoku import ichimoku

class Ichimoku:
    @staticmethod
    def init(symbol, state: StrategyState):
        state.variables['history'] = state.interface.history(symbol, resolution=state.resolution, return_as='df')
        state.variables['prev_price'] = state.variables['history']['close'].iloc[-2]
        state.variables['current_price'] = state.variables['history']['close'].iloc[-1]

    @staticmethod
    def price_event(price, symbol, state: StrategyState):
        h = state.interface.history(symbol, resolution=state.resolution, return_as='df')
        state.variables['history'] = h # appends to the deque of historical prices
        prev_price = state.variables['current_price']
        state.variables['prev_price'] = prev_price
        state.variables['current_price'] = price

        signal = ichimoku(h)
        if signal["tenkan_sen"] > signal["kijun_sen"] and prev_price < signal["senkou_span_a"] and price > signal["senkou_span_a"]:
            buy = int(state.interface.cash / price)
            state.interface.market_order(symbol, side='buy', size=buy)
            state.variables['owns_position'] = True
        elif signal["tenkan_sen"] < signal["kijun_sen"] and prev_price > signal["senkou_span_a"] and price < signal["senkou_span_a"]:
            curr_value = int(state.interface.account[state.base_asset].available)
            state.interface.market_order(symbol, side='sell', size=curr_value)
            state.variables['owns_position'] = False
