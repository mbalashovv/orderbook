from dash import Dash

from .app import App

__all__ = ("get_app", )


def get_app() -> Dash:
    return App().get_app()
