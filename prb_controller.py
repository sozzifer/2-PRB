import plotly.graph_objects as go
from dash import Input, Output, State, exceptions, no_update
from prb_view import app
from prb_model import generate_draws


@app.callback(
    Output("interval", "n_intervals"),
    Output("interval", "max_intervals"),
    Output("draw-store", "data"),
    Output("win-store", "data"),
    Output("prob-store", "data"),
    Output("win-rate-store", "data"),
    Output("my-tickets-store", "data"),
    Output("winning-ticket-store", "data"),
    Output("stop", "n_clicks"),
    Output("num-tickets", "invalid"),
    Input("draw", "n_clicks"),
    Input("stop", "n_clicks"),
    State("num-tickets", "value"),
    State("total-tickets", "value"),
    State("num-draws", "value"),
    prevent_initial_call=True
)
def update_stores(n_clicks_draw, n_clicks_stop, num, total, draws):
    if n_clicks_draw is None:
        raise exceptions.PreventUpdate
    elif num > total:
        return no_update,\
            no_update,\
            no_update,\
            no_update,\
            no_update,\
            no_update,\
            no_update,\
            no_update,\
            no_update,\
            True
    else:
        n_intervals = 0
        max_intervals = draws + 1
        _, my_tickets_string_list, winning_ticket_list, draw_list, win_list, prob_list, win_rate = generate_draws(num, total, draws)
        if n_clicks_stop == 1:
            max_intervals = 0
            n_clicks_stop = 0
        return n_intervals,\
            max_intervals,\
            draw_list,\
            win_list,\
            prob_list,\
            win_rate,\
            my_tickets_string_list,\
            winning_ticket_list,\
            n_clicks_stop,\
            False


@app.callback(
    Output("graph", "figure"),
    Output("probability", "children"),
    Output("win-rate", "children"),
    Output("draws", "children"),
    Output("sr-graph", "children"),
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
        fig.update_yaxes(
            range=[-0.1, max(win_list[-1]+0.1, prob_list[-1]+0.1)])
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
        win_rate = win_rate
        draws = draw_list[n_intervals-1]
        sr_graph = f"Line chart showing the observed win rate and expected win rate after {draws} draws"
        return fig, f"{probability:.2%}", f"{win_rate:.2%}", f"{draws}", sr_graph
    except:
        return no_update, no_update, no_update, no_update, no_update


@app.callback(
    Output("interval", "interval"),
    Input("slider", "value")
)
def set_draw_speed(value):
    return 1000/value


if __name__ == "__main__":
    # app.run(debug=False, host="0.0.0.0", port=8080, dev_tools_ui=False)
    app.run(debug=True)
