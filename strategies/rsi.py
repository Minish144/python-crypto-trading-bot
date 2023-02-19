from blankly import StrategyState
import blankly

class RSI:
    @staticmethod
    def init(symbol, state: StrategyState):
        state.variables['history'] = state.interface.history(symbol, to=150, return_as='deque')['close']
        state.variables['owns_position'] = False

    @staticmethod
    def price_event(price, symbol, state: StrategyState):
        state.variables['history'].append(price) # appends to the deque of historical prices
        rsi = blankly.indicators.rsi(state.variables['history'])
        if rsi[-1] < 30 and not state.variables['owns_position']:
            buy = int(state.interface.cash / price)
            state.interface.market_order(symbol, side='buy', size=buy)
            state.variables['owns_position'] = True
        elif rsi[-1] > 70 and state.variables['owns_position']:
            curr_value = int(state.interface.account[state.base_asset].available)
            state.interface.market_order(symbol, side='sell', size=curr_value)
            state.variables['owns_position'] = False
