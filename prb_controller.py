from dash import Input, Output, State, exceptions, no_update
import plotly.graph_objects as go
from prb_view import app
from prb_model import generate_draws

# app.callback Outputs and Inputs are all associated with unique elements in *_view.py though the first argument (component_id) and control/are controlled by the second argument (component_property)


# Populate dcc.Interval and dcc.Store components so that the animated graph can be generated from the stored data
@app.callback(
    # dcc.Interval component
    Output("interval", "n_intervals"),
    Output("interval", "max_intervals"),
    # dcc.Store components
    Output("draw-store", "data"),
    Output("win-store", "data"),
    Output("prob-store", "data"),
    Output("win-rate-store", "data"),
    # Input validation
    Output("num-tickets", "invalid"),
    # Inputs
    Input("draw", "n_clicks"),
    State("num-tickets", "value"),
    State("total-tickets", "value"),
    State("num-draws", "value"),
    prevent_initial_call=True
)
def update_stores(n_clicks_draw, num, total, draws):
    if n_clicks_draw is None:
        raise exceptions.PreventUpdate
    # Input validation
    elif num > total:
        return no_update,\
            no_update,\
            no_update,\
            no_update,\
            no_update,\
            no_update,\
            True
    else:
        n_intervals = 0
        max_intervals = draws + 1
        draw_list, win_list, prob_list, win_rate = generate_draws(num, total, draws)
        return n_intervals,\
            max_intervals,\
            draw_list,\
            win_list,\
            prob_list,\
            win_rate,\
            False


# Callback function to generate animated graph (using dcc.Interval and dcc.Store data) and update results and screen reader text
@app.callback(
    # Graph Outputs
    Output("graph", "figure"),
    Output("sr-graph", "children"),
    # Results Outputs
    Output("probability", "children"),
    Output("win-rate", "children"),
    Output("draws", "children"),
    # Inputs
    Input("interval", "n_intervals"),
    Input("draw-store", "data"),
    Input("win-store", "data"),
    Input("prob-store", "data"),
    Input("win-rate-store", "data"),
    prevent_initial_call=True
)
def update_graph(n_intervals, draw_list, win_list, prob_list, win_rate):
    try:
        fig = go.Figure(
            go.Scatter(x=[], y=[]),
            layout={"margin": dict(t=20, b=10, l=20, r=20),
                    "height": 375,
                    "xaxis_title": "Number of draws",
                    "yaxis_title": "Wins",
                    "font_size": 14})
        fig.update_xaxes(range=[-0.1, len(draw_list)-0.9])
        fig.update_yaxes(range=[-0.1, max(win_list[-1]+0.1, prob_list[-1]+0.1)])
        fig.update_layout(dragmode=False)
        # If observed and expected win lists are identical, expected wins are displayed as points rather than a line to make the visualisation clearer
        if win_list == prob_list:
            fig.add_trace(
                go.Scatter(x=draw_list[0:n_intervals],
                           y=win_list[0:n_intervals],
                           name="Observed wins",
                           mode="lines",
                           marker_color="#9eab05",
                           hovertemplate="Number of observed wins: %{y}<br>Number of draws: %{x}<extra></extra>"))
            fig.add_trace(
                go.Scatter(x=draw_list[0:n_intervals],
                           y=prob_list[0:n_intervals],
                           name="Expected wins",
                           mode="markers",
                           marker_color="#d10373",
                           hovertemplate="Number of expected wins: %{y}<br>Number of draws: %{x}<extra></extra>"))
        else:
            fig.add_trace(
                go.Scatter(x=draw_list[0:n_intervals],
                           y=win_list[0:n_intervals],
                           name="Observed wins",
                           mode="lines",
                           marker_color="#9eab05",
                           hovertemplate="Number of observed wins: %{y}<br>Number of draws: %{x}<extra></extra>"))
            fig.add_trace(
                go.Scatter(x=draw_list[0:n_intervals],
                           y=prob_list[0:n_intervals],
                           name="Expected wins",
                           mode="lines",
                           marker_color="#d10373",
                           hovertemplate="Number of expected wins: %{y}<br>Number of draws: %{x}<extra></extra>"))
        probability = prob_list[1]
        draws = draw_list[n_intervals-1]
        # Screen reader text
        sr_graph = f"Line chart showing the observed win rate {win_rate:.2%} and expected win rate {probability:.2%} after {draws} draws"
        return fig, sr_graph, f"{probability:.2%}", f"{win_rate:.2%}", f"{draws}"
    except:
        return no_update, no_update, no_update, no_update, no_update


# Set draw rate for graph animation
@app.callback(
    Output("interval", "interval"),
    Input("slider", "value")
)
def set_draw_speed(value):
    return 1000/value


if __name__ == "__main__":
    # app.run(debug=True)
    # To deploy on Docker, replace app.run(debug=True) with the following:
    app.run(debug=False, host="0.0.0.0", port=8080, dev_tools_ui=False)
