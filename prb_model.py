import numpy as np
import random
import plotly.graph_objects as go


def generate_draws(num, total, draws):
    draws = list(range(1, draws + 1))
    probability = num/total
    my_tickets_list = []
    tickets_string_list = []
    my_tickets_string_list = []
    winning_ticket_list = []
    win_list = [0]
    draw_list = [0]
    prob_list = [0]
    win_rate = 0
    for draw in draws:
        winner = False
        my_tickets = random.sample(range(1, int(total) + 1), int(num))
        my_tickets_list.append(my_tickets)
        tickets_string = [str(x) for x in my_tickets]
        tickets_string_list.append(tickets_string)
        my_tickets_string = ", ".join(tickets_string)
        my_tickets_string_list.append(my_tickets_string)
        winning_ticket = np.random.randint(1, int(total) + 1)
        winning_ticket_list.append(winning_ticket)
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
    return my_tickets_list,\
           my_tickets_string_list,\
           winning_ticket_list,\
           draw_list,\
           win_list,\
           prob_list,\
           win_rate


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
