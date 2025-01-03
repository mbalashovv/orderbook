import requests
from dash import Dash, html, dcc, Input, Output, dash_table

from src.pkg.settings import Settings

__all__ = (
    "update_mid_price_style",
    "table_styling",
    "dropdown_option",
    "get_pairs",
)


current_mid_price = 0


def update_mid_price_style(new_price) -> list[dict]:
    global current_mid_price

    mid_price_style = {"font-size": "32px", "margin-bottom": "0px"}
    mid_price_sign_style = {"font-size": "32px", "line-height": "0px"}

    if new_price > current_mid_price:
        mid_price_style["color"] = mid_price_sign_style["color"] = "rgb(13, 230, 49)"
        mid_price_sign_style["rotate"] = "180deg"
    elif new_price < current_mid_price:
        mid_price_style["color"] = mid_price_sign_style["color"] = "rgb(230, 31, 7)"
    else:
        mid_price_style["color"] = "white"
        mid_price_sign_style["display"] = "none"

    current_mid_price = new_price

    return [
        mid_price_style,
        mid_price_sign_style
    ]


def table_styling(df, side) -> list[dict]:
    bar_color = "rgba(230, 31, 7, 0.2)" if side == "bid" else "rgba(13, 230, 49, 0.2)"
    font_color = "rgb(230, 31, 7)" if side == "bid" else "rgb(13, 230, 49)"
    cell_bg_color = "#060606"

    n_bins = 25
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    quantity = df.quantity.astype(float)
    ranges = [((quantity.max() - quantity.min()) * i) + quantity.min() for i in bounds]

    styles = []

    for i in range(1, len(bounds)):  # TODO: may slow down the program
        min_bound = ranges[i-1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100

        styles.append(
            {
                "if": {
                    "filter_query": ("{{quantity}} >= {min_bound}" +
                                     (" && {{quantity}} < {max_bound}" if ((i < len(bounds)) - 1) else "")).format(min_bound=min_bound, max_bound=max_bound),
                    "column_id": "quantity"
                },
                "background": (
                    f"""
                        linear-gradient(
                            270deg, 
                            {bar_color} 0%, 
                            {bar_color} {max_bound_percentage}%, 
                            {cell_bg_color} {max_bound_percentage}%, 
                            {cell_bg_color} 100%
                        )
                    """.format(
                        bar_color=bar_color,
                        cell_bg_color=cell_bg_color,
                        max_bound_percentage=max_bound_percentage
                    ),
                ),
                "paddingBottom": 2,
                "paddingTop": 2,
            }
        )

    styles.append(
        {
            "if": {"column_id": "price"},
            "color": font_color,
            "background-color": cell_bg_color,
        }
    )
    return styles


def dropdown_option(title, options, default_value, id_, searchable=False):
    return html.Div(
        children=[
            html.H2(title),
            dcc.Dropdown(
                options=options, value=default_value, id=id_, searchable=searchable,
            ),
        ]
    )


def get_pairs() -> list[str]:
    data = requests.get(f"{Settings.API_URL}/v5/market/tickers", params={"category": Settings.API_ORDERS_CATEGORY}).json()
    pairs = [a["symbol"] for a in data["result"]["list"]]
    pairs.sort()
    return pairs