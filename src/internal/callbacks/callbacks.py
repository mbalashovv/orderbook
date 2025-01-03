import requests
import pandas as pd
from decimal import Decimal
from dash import Dash, html, dcc, Input, Output, dash_table

from src.internal.services.layout import (
    table_styling,
    update_mid_price_style,
)
from src.internal.services.orderbook import aggregate_levels

from src.pkg.settings import Settings

__all__ = ("register_callbacks", )


def register_callbacks(app: Dash):
    @app.callback(
        Output("bid_table", "data"),
        Output("bid_table", "style_data_conditional"),
        Output("ask_table", "data"),
        Output("ask_table", "style_data_conditional"),
        Output("orderbook_data", "data"),
        Input("aggregation_level", "value"),
        Input("pair", "value"),
        Input("quantity_precision", "value"),
        Input("price_precision", "value"),
        Input("timer", "n_intervals"),
    )
    def update_orderbook(agg_level, symbol, quantity_precision, price_precision, n_intervals):
        data = requests.get(
            f"{Settings.API_URL}/v5/market/orderbook",
            params={
                "category": Settings.API_ORDERS_CATEGORY,
                "symbol": symbol.upper(),
                "limit": Settings.API_ORDERS_LIMIT,
            }
        ).json()

        bid_df = pd.DataFrame(data["result"]["b"], columns=["price", "quantity"], dtype=float)
        ask_df = pd.DataFrame(data["result"]["a"], columns=["price", "quantity"], dtype=float)

        mid_price = (bid_df.price.iloc[0] + ask_df.price.iloc[0]) / 2

        bid_df = aggregate_levels(bid_df, agg_level=Decimal(agg_level), side="bid")
        bid_df = bid_df.sort_values("price", ascending=False)

        ask_df = aggregate_levels(ask_df, agg_level=Decimal(agg_level), side="ask")
        ask_df = ask_df.sort_values("price", ascending=False)

        bid_df = bid_df.iloc[:Settings.ORDERBOOK_LEVELS_TO_SHOW]
        ask_df = ask_df.iloc[-Settings.ORDERBOOK_LEVELS_TO_SHOW:]

        bid_df.quantity = bid_df.quantity.apply(
            lambda x: f"%.{quantity_precision}f" % x
        )

        bid_df.price = bid_df.price.apply(
            lambda x: f"%.{price_precision}f" % x
        )

        ask_df.quantity = ask_df.quantity.apply(
            lambda x: f"%.{quantity_precision}f" % x
        )

        ask_df.price = ask_df.price.apply(
            lambda x: f"%.{price_precision}f" % x
        )

        return (
            bid_df.to_dict("records"),
            table_styling(bid_df, "bid"),
            ask_df.to_dict("records"),
            table_styling(ask_df, "ask"),
            mid_price,
        )


    @app.callback(
        Output("mid_price", "children"),
        Output("mid_price", "style"),
        Output("mid_price_sign", "style"),
        Input("orderbook_data", "data"),
        Input("price_precision", "value"),
    )
    def update_mid_price(mid_price, price_precision):
        mid_price_style, mid_price_sign_style = update_mid_price_style(mid_price)
        mid_price_precision = int(price_precision) + 2
        mid_price = f"%.{mid_price_precision}f" % mid_price

        return (
            mid_price,
            mid_price_style,
            mid_price_sign_style,
        )

