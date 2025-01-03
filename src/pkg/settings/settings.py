__all__ = ("Settings", )

class App:
    APP_DEBUG = True
    APP_PORT = 8050
    APP_UPDATE_INTERVAL_MS = 3000


class API:
    API_URL = "https://api.bybit.com"
    API_ORDERS_LIMIT = 200
    API_ORDERS_CATEGORY = "spot"


class OrderBook:
    ORDERBOOK_LEVELS_TO_SHOW = 10
    ORDERBOOK_AGGREGATION_LEVELS = ["0.01", "0.1", "1", "10", "100"]
    ORDERBOOK_QUANTITY_PRECISION = ["0", "1", "2", "3", "4"]
    ORDERBOOK_PRICE_PRECISION = ["0", "1", "2", "3", "4"]


class Settings(App, API, OrderBook): ...
