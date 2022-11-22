from dash import dcc, html
from app import app

layout = html.Div(
    [
        html.Div(
            dcc.Markdown(
                """
                # About this app
                This page will offer a quick overview of the app and its main features.
                
                As I am in the process of writing this page, I would appreciate any feedback you may have.
                
                """
            )
        )
    ]
)
