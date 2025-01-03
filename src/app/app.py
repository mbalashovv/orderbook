import dash_bootstrap_components as dbc

from dash import Dash, html, dcc, Input, Output, dash_table

from src.internal.services.layout import dropdown_option, get_pairs
from src.internal.callbacks import register_callbacks
from src.pkg.settings import Settings

__all__ = ("App", )


class App:
    __app: Dash

    def __init__(self):
        self.__app = Dash(external_stylesheets=[dbc.themes.CYBORG, dbc.icons.BOOTSTRAP])
        self._set_layout()
        self._register_callbacks()


    def _set_layout(self) -> None:
        self.__app.layout = html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                dash_table.DataTable(
                                    id="ask_table",
                                    style_header={"display": "none"},
                                    style_cell={
                                        "minWidth": "140px",
                                        "maxWidth": "140px",
                                        "width": "140px",
                                        "text-align": "right",
                                        "padding-right": "10px",
                                    },
                                ),

                                html.Div(
                                    children=[
                                        html.I(id="mid_price_sign", className="bi bi-arrow-down-short", style={"display": "none"}),
                                        html.H3(id="mid_price", style={"font-size": "32px", "margin-bottom": "0px"}),
                                    ],
                                    style={
                                        "display": "flex",
                                        "padding-top": "30px",
                                        "align-items": "flex-end",
                                    }
                                ),

                                dash_table.DataTable(
                                    id="bid_table",
                                    style_header={"display": "none"},
                                    style_cell={
                                        "minWidth": "140px",
                                        "maxWidth": "140px",
                                        "width": "140px",
                                        "text-align": "right",
                                        "padding-right": "10px",
                                    },
                                ),
                            ], style={
                                "width": "300px",
                                "display": "flex",
                                "flex-direction": "column",
                                "align-items": "flex-end",
                            }
                        ),
                        html.Div(
                            children=[
                                dropdown_option(
                                    "Aggregate Level",
                                    options=Settings.ORDERBOOK_AGGREGATION_LEVELS,
                                    default_value="0.01",
                                    id_="aggregation_level",
                                ),
                                dropdown_option(
                                    title="Pair",
                                    options=get_pairs(),
                                    default_value="BTCUSDT",
                                    id_="pair",
                                    searchable=True,
                                ),
                                dropdown_option(
                                    title="Quantity Precision",
                                    options=Settings.ORDERBOOK_QUANTITY_PRECISION,
                                    default_value="2",
                                    id_="quantity_precision",
                                ),
                                dropdown_option(
                                    title="Price Precision",
                                    options=Settings.ORDERBOOK_PRICE_PRECISION,
                                    default_value="2",
                                    id_="price_precision",
                                ),
                            ],
                            style={"display": "flex", "flex-direction": "column", "gap": "10px"}
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                        "height": "100vh",
                        "gap": "100px",
                    }
                ),
                dcc.Store(id="orderbook_data", storage_type="memory"),
                dcc.Interval(id="timer", interval=Settings.APP_UPDATE_INTERVAL_MS),
            ]
        )

    def _register_callbacks(self) -> None:
        register_callbacks(app=self.__app)

    def get_app(self) -> Dash:
        return self.__app
