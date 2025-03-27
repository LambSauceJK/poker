from dash import Dash, Input, Output, dcc, html
import dash
import plotly.graph_objs as go
import poker_game as pg
import bot_players as bots

# Initialize the app
app = Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1('Play Poker against a Bot'),
    html.P('Select a bot:'),
    dcc.Dropdown(
        id='bot-dropdown',
        options=[
            {'label': 'EV Bot', 'value': 'EVBot'},
            {'label': 'Hazard Bot', 'value': 'HazardBot'},
            {'label': 'Cheater Bot', 'value': 'CheaterBot'}
        ],
        value='EVBot'
    ),
    html.P('Your current balance: $1000'),
    html.Button('Play Hand', id='play-button', n_clicks=0),
    html.Div(id='game-state'),
    dcc.Graph(id='balance-graph')
])

# Define the callback for the play button
@app.callback(
    Output('game-state', 'children'),
    [Input('play-button', 'n_clicks')],
    [dash.dependencies.State('bot-dropdown', 'value')]
)
def play_hand(n_clicks, bot_value):
    if n_clicks is not None and n_clicks > 0:
        # Initialize the game and bot
        game = pg.PokerGame()
        bot_class = getattr(bots, bot_value)
        bot = bot_class(game)

        # Play a hand
        game.initialise_players([bot], shuffle=False)
        game.run_hands(n=1)

        # Get the game state
        game_state = game.history[0]

        # Return the game state as a string
        return f'You won ${game_state} this hand!'

# Define the callback for the balance graph
@app.callback(
    Output('balance-graph', 'figure'),
    [Input('play-button', 'n_clicks')],
    [dash.dependencies.State('bot-dropdown', 'value')]
)
def update_balance_graph(n_clicks, bot_value):
    if n_clicks is not None and n_clicks > 0:
        # Initialize the game and bot
        game = pg.PokerGame()
        bot_class = getattr(bots, bot_value)
        bot = bot_class(game)

        # Play a hand
        game.initialise_players([bot], shuffle=False)
        game.run_hands(n=n_clicks)

        # Get the balance history
        balance_history = game.history[0]

        # Create the figure
        fig = go.Figure(data=[go.Scatter(x=list(range(n_clicks)), y=balance_history)])
        fig.update_layout(title='Balance History', xaxis_title='Hand Number', yaxis_title='Balance')

        # Return the figure
        return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)