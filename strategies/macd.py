from blankly import StrategyState
import blankly

SHORT_PERIOD = 12
LONG_PERIOD = 26
SIGNAL_PERIOD = 9

class MACD:
    @staticmethod
    def init(symbol, state: StrategyState):
        state.variables['history'] = state.interface.history(symbol, 800, state.resolution, return_as='list')['close']
        state.variables['short_period'] = SHORT_PERIOD
        state.variables['long_period'] = LONG_PERIOD
        state.variables['signal_period'] = SIGNAL_PERIOD
        state.variables['has_bought'] = False

    @staticmethod
    def price_event(price, symbol, state: StrategyState):
        state.variables['history'].append(price)
        macd_res, macd_signal, _ = blankly.indicators.macd(data=state.variables['history'],
                                                           short_period=state.variables['short_period'],
                                                           long_period=state.variables['long_period'],
                                                           signal_period=state.variables['signal_period'])

        slope_macd = (macd_res[-1] - macd_res[-5]) / 5  # get the slope of the last 5 MACD_points
        prev_macd = macd_res[-2]
        curr_macd = macd_res[-1]
        curr_signal_macd = macd_signal[-1]

        # We want to make sure this works even if curr_macd does not equal the signal MACD
        is_cross_up = slope_macd > 0 and curr_macd >= curr_signal_macd > prev_macd

        is_cross_down = slope_macd < 0 and curr_macd <= curr_signal_macd < prev_macd
        if is_cross_up and not state.variables['has_bought']:
            # buy with all available cash
            buy = blankly.trunc(state.interface.cash / price, 2)
            state.interface.market_order(symbol, side='buy', size=buy)
            state.variables['has_bought'] = True
        elif is_cross_down and state.variables['has_bought']:
            cur_value = blankly.trunc(state.interface.account[state.base_asset].available, 2)
            state.interface.market_order(symbol, side='sell', size=cur_value)
            state.variables['has_bought'] = False
