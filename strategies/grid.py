import blankly
from blankly import StrategyState

class Grid:
    @staticmethod
    def init(retry_timeout, base_order_size, grid_spacing_percent, num_grid_above_below):
        def closure(symbol, state: StrategyState):
            state.variables['retry_timeout'] = retry_timeout
            state.variables['base_order_size'] = base_order_size
            state.variables['grid_spacing_percent'] = grid_spacing_percent
            state.variables['num_grid_above_below'] = num_grid_above_below
            state.variables['last_try'] = state.time
        return closure

    @staticmethod
    def price_event(price, symbol, state: StrategyState):
        now = state.time

        orders = state.interface.get_open_orders(symbol)
        if len(orders) > 0:
            if now - state.variables['last_try'] < state.variables['retry_timeout']:
                return

            for order in orders:
                state.interface.cancel_order(symbol, order_id=order['id'])


        state.variables['last_try'] = now

        buy_grids, sell_grids = generate_grid(price, state.variables['num_grid_above_below'], state.variables['grid_spacing_percent'])

        for i in range(len(buy_grids)):
            try:
                buy_price = blankly.trunc(buy_grids[i], 2)
                state.interface.limit_order(symbol, 'buy', buy_price, state.variables['base_order_size'])
                print("new buy order", "size: ", state.variables['base_order_size'], "price", buy_price)
            except Exception as e:
                print('"failed to place order"', '"error"', e, "price", buy_price, buy_grids[i])

            try:
                sell_price = blankly.trunc(sell_grids[i], 2)
                state.interface.limit_order(symbol, 'sell', sell_price, state.variables['base_order_size'])
                print("new sell order", "size: ", state.variables['base_order_size'], "price", sell_price)
            except Exception as e:
                print('"failed to place order"', '"error"', e, "price", sell_price, sell_grids[i])

def generate_grid(price, num_grid_above_below, grid_spacing_percent):
    buy_grid = []
    sell_grid = []

    for i in range(num_grid_above_below):
        price_above = price * (1 + grid_spacing_percent / 100) ** (i + 1)
        price_below = price * (1 - grid_spacing_percent / 100) ** (i + 1)
        sell_grid.append(price_above)
        buy_grid.append(price_below)

    return buy_grid, sell_grid

