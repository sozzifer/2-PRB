import numpy as np
import plotly.graph_objects as go
import random

# Generate data to update graph and results based on user entry (number of tickets bought, total number of tickets, number of draws)
def generate_draws(num, total, draws):
    draws = list(range(1, draws + 1))
    probability = num/total
    win_list = [0]
    draw_list = [0]
    prob_list = [0]
    win_rate = 0
    for draw in draws:
        winner = False
        my_tickets = random.sample(range(1, int(total) + 1), int(num))
        winning_ticket = np.random.randint(1, int(total) + 1)
        for ticket in my_tickets:
            if ticket == winning_ticket:
                winner = True
        if winner == True:
            win_list.append(win_list[-1] + 1)
        else:
            win_list.append(win_list[-1])
        prob_list.append(prob_list[-1] + probability)
        draw_list.append(draw)
        win_rate = win_list[-1]/draw_list[-1]
    return draw_list,\
           win_list,\
           prob_list,\
           win_rate

# Replace default go.Figure with blank go.Scatter plot (UX)
def create_blank_fig():
    blank_fig = go.Figure(
        go.Scatter(x=[],
                   y=[]),
        layout={"margin": dict(t=20, b=10, l=20, r=20),
                "height": 375,
                "xaxis_title": "Number of draws",
                "yaxis_title": "Wins",
                "font_size": 14})
    blank_fig.update_xaxes(range=[0, 5])
    blank_fig.update_yaxes(range=[0, 3])
    return blank_fig
