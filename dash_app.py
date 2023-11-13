# Import necessary libraries
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output

# Create a Dash application
app = Dash(__name__)

# Read data from an Excel file for both sheets
active_retire_df = pd.read_excel('mil_pay.xlsx', sheet_name='ActiveRetire')
reserve_retire_df = pd.read_excel('mil_pay.xlsx', sheet_name='ReserveRetire')

# Active retirement graph initial values
active_retire_default_start_year = active_retire_df['Military Pay'].diff().idxmin() if active_retire_df['Military Pay'].diff().idxmin() is not None else active_retire_df['Military Pay'].last_valid_index() + 1
active_retire_default_amount = active_retire_df['Military Pay'].max() if active_retire_df['Military Pay'].max() is not None else 80000
active_retire_default_end_year = active_retire_df['Gov\'t TSP Payout'].first_valid_index() - 1

# Reserve retirement graph initial values
reserve_retire_default_start_year = reserve_retire_df['Military Pay'].diff().idxmin() if reserve_retire_df['Military Pay'].diff().idxmin() is not None else reserve_retire_df['Military Pay'].last_valid_index() + 1
reserve_retire_default_amount = reserve_retire_df['Military Pay'].max() if reserve_retire_df['Military Pay'].max() is not None else 80000
reserve_retire_default_end_year = reserve_retire_df['Gov\'t TSP Payout'].first_valid_index() - 1

# Initialize a new column 'Post Mil Retirement Pay' with zeros
active_retire_df['Post Mil Retirement Pay'] = 0
reserve_retire_df['Post Active Duty Pay'] = 0

# Define the columns to be included in the visualization
active_retire_selected_columns = ['Military Pay', 'Bonus & Payments', 'BRS Pension', 'Service Member TSP Payout', "Gov't TSP Payout", 'Post Mil Retirement Pay']
reserve_retire_selected_columns = ['Military Pay', 'Bonus & Payments', 'BRS Pension', 'Service Member TSP Payout', "Gov't TSP Payout", 'Post Active Duty Pay']

# Define the layout of the app
app.layout = html.Div([
    html.H1("Active and Reserve Retirement Lifetime Pay Comparison"),

    # Active retirement graph options
    html.Div([
    html.Label('Active retirement graph post-military retirement pay options: '),

    html.Div([
        html.Label('Start year: ', style={'display': 'inline-block', 'width': '75px'}),
        dcc.Input(id='active_retire_start_year_input', type='number', value=active_retire_default_start_year),
    ]),

    html.Div([
        html.Label('Amount: ', style={'display': 'inline-block', 'width': '75px'}),
        dcc.Input(id='active_retire_amount_input', type='number', value=active_retire_default_amount),
    ]),

    html.Div([
        html.Label('End year: ', style={'display': 'inline-block', 'width': '75px'}),
        dcc.Input(id='active_retire_end_year_input', type='number', value=active_retire_default_end_year),
    ]),

    html.Div(id='active_retire_lifetime_earnings'),

    ], style={'margin-bottom': '20px', 'border': '1px solid #ddd', 'padding': '10px'}),

    # Active retirement graph
    dcc.Graph(id='active_retire_graph'),

    # Reserve retirement graph options
    html.Div([
    html.Label('Reserve retirement graph post-active duty pay options: '),

    html.Div([
        html.Label('Start year: ', style={'display': 'inline-block', 'width': '75px'}),
        dcc.Input(id='reserve_retire_start_year_input', type='number', value=reserve_retire_default_start_year),
    ]),

    html.Div([
        html.Label('Amount: ', style={'display': 'inline-block', 'width': '75px'}),
        dcc.Input(id='reserve_retire_amount_input', type='number', value=reserve_retire_default_amount),
    ]),

    html.Div([
        html.Label('End year: ', style={'display': 'inline-block', 'width': '75px'}),
        dcc.Input(id='reserve_retire_end_year_input', type='number', value=reserve_retire_default_end_year),
    ]),

    html.Div(id='reserve_retire_lifetime_earnings'),

    ], style={'margin-bottom': '20px', 'border': '1px solid #ddd', 'padding': '10px'}),

    # Reserve retirement graph
    dcc.Graph(id='reserve_retire_graph'),
])

# Create callback functions to update the graphs for ActiveRetire and ReserveRetire sheets
@app.callback(
    [Output('active_retire_graph', 'figure'),
    Output('active_retire_lifetime_earnings', 'children')],
    [Input('active_retire_start_year_input', 'value'),
     Input('active_retire_amount_input', 'value'),
     Input('active_retire_end_year_input', 'value')]
)
def update_active_retire_graph(start_year, amount, end_year):
    end_year = min(end_year, active_retire_default_end_year)  # Ensure end_year is within bounds
    active_retire_df.loc[start_year:end_year, 'Post Mil Retirement Pay'] = amount

    data = []
    lifetime_earnings = 0

    for column in active_retire_selected_columns:
        trace = go.Bar(
            x=active_retire_df['Calendar Year'],
            y=active_retire_df[column],
            name=column
        )
        data.append(trace)

        lifetime_earnings += active_retire_df[column].sum()

    layout = go.Layout(
        barmode='stack',
        title='Active Retirement Graph',
        yaxis=dict(range=[0,250000])
    )

    fig = go.Figure(data=data, layout=layout)

    lifetime_earnings = "${:,.2f}".format(lifetime_earnings)

    lifetime_earnings_div = html.Div(
        children=[
            html.Div("Lifetime Earnings", style={'font-weight': 'bold'}),
            html.Div(lifetime_earnings, style={'border': '2px solid black', 'padding': '10px'})
        ]
    )

    return fig, lifetime_earnings_div

@app.callback(
    [Output('reserve_retire_graph', 'figure'),
     Output('reserve_retire_lifetime_earnings', 'children')],
    [Input('reserve_retire_start_year_input', 'value'),
     Input('reserve_retire_amount_input', 'value'),
     Input('reserve_retire_end_year_input', 'value')]
)
def update_reserve_retire_graph(start_year, amount, end_year):
    end_year = min(end_year, reserve_retire_default_end_year)  # Ensure end_year is within bounds
    reserve_retire_df.loc[start_year:end_year, 'Post Active Duty Pay'] = amount

    data = []
    lifetime_earnings = 0

    for column in reserve_retire_selected_columns:
        trace = go.Bar(
            x=reserve_retire_df['Calendar Year'],
            y=reserve_retire_df[column],
            name=column
        )
        data.append(trace)

        lifetime_earnings += reserve_retire_df[column].sum()

    layout = go.Layout(
        barmode='stack',
        title='Reserve Retirement Graph',
        yaxis=dict(range=[0,250000])
    )

    fig = go.Figure(data=data, layout=layout)

    lifetime_earnings = "${:,.2f}".format(lifetime_earnings)

    lifetime_earnings_div = html.Div(
        children=[
            html.Div("Lifetime Earnings", style={'font-weight': 'bold'}),
            html.Div(lifetime_earnings, style={'border': '2px solid black', 'padding': '10px'})
        ]
    )

    return fig, lifetime_earnings_div

# Run the app if this script is the main entry point
if __name__ == '__main__':
    app.run_server(debug=True)
