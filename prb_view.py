from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from prb_model import create_blank_fig

# Specify HTML <head> elements
app = Dash(__name__,
           title="Probability",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

# Specify app layout (HTML <body> elements) using dash.html, dash.dcc and dash_bootstrap_components
# All component IDs should relate to the Input or Output of callback functions in *_controller.py
app.layout = dbc.Container([
    # Data Stores, Instructions, Results and Graph
    dbc.Row([
        dcc.Interval(id="interval",
                     interval=1000,
                     max_intervals=0),
        dcc.Store(id="draw-store"),
        dcc.Store(id="win-store"),
        dcc.Store(id="prob-store"),
        dcc.Store(id="win-rate-store"),
        dbc.Col([
            dbc.Card([
                dbc.CardBody(children=[
                    "The probability of winning a raffle with n tickets, where you buy x tickets, and one winning ticket is drawn, is x/n.",
                    html.Br(),
                    html.Br(),
                    "Enter the number of tickets bought (x) and the total number of tickets (n), and set the number of draws as 10. Is the observed win rate the same as the expected win rate? What about if you draw 20 times? 50 times?"])]),
            dbc.Card([
                dbc.CardBody([
                    html.H4("Results"),
                    html.Div([
                        html.P(children=[
                            html.Span("Expected win rate: ", className="bold-p"),
                            html.Span(id="probability")
                        ]),
                        html.P(children=[
                            html.Span("Observed win rate: ", className="bold-p"),
                            html.Span(id="win-rate")
                        ]),
                        html.P(children=[
                            html.Span("Draws: ", className="bold-p"),
                            html.Span(id="draws")
                        ])
                    ], **{"aria-live": "polite"})
                ])
            ])
        ], xs=12, sm=12, md=12, lg=5, xl=5),
        dbc.Col([
            # Graph components are placed inside a Div with role="img" to manage the experience for screen reader users
            html.Div([
                dcc.Graph(id="graph",
                          figure=create_blank_fig(),
                          config={"displayModeBar": False,
                                  "doubleClick": False,
                                  "editable": False,
                                  "scrollZoom": False,
                                  "showAxisDragHandles": False})
            ], role="img", style={"height": 350}, **{"aria-hidden": "true"}),
            # A second Div is used to associate alt text with the relevant Graph component to manage the experience for screen reader users, styled using CSS
            html.Div(id="sr-graph",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"}),
            html.Br(),
        ], xs=12, sm=12, md=12, lg=7, xl=7)
    ]),
    # User Input
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label("Enter number of tickets bought, x (max 1000)",
                          class_name="label",
                          html_for="num-tickets"),
                dbc.Input(id="num-tickets",
                          value=3,
                          type="number",
                          min=1,
                          max=1000,
                          step=1,
                          required=True,
                          invalid=False),
                dbc.FormFeedback("Number of tickets bought must be less than total tickets",
                                 type="invalid")
            ], **{"aria-live": "polite"}),
            dbc.Label("Enter total number of tickets, n (max 1000)",
                      class_name="label",
                      html_for="total-tickets"),
            dbc.Input(id="total-tickets",
                      value=10,
                      type="number",
                      min=1,
                      max=1000,
                      step=1,
                      required=True),
            dbc.Label("Enter number of draws (max 100)",
                      class_name="label",
                      html_for="num-draws"),
            dbc.Input(id="num-draws",
                      value=10,
                      type="number",
                      min=1,
                      max=100,
                      step=1,
                      required=True)
        ], xs=12, sm=12, md=12, lg=5, xl=5),
        dbc.Col([
            dbc.Label("Set number of draws per second",
                       class_name="label",
                       html_for="slider"),
            dcc.Slider(id="slider",
                       min=10,
                       max=30,
                       step=5,
                       value=10),
            html.Div([
                dbc.Button(id="draw",
                           n_clicks=0,
                           children="Draw",
                           class_name="button")
            ], className="d-flex justify-content-center", style={"margin": "0 auto"}),
        ], xs=12, sm=12, md=12, lg=7, xl=7)
    ])
], fluid=True)
