# Import necessary libraries
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
from dash.exceptions import PreventUpdate

# Set the style for the page
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Create a Dash application
app = Dash(__name__, external_stylesheets=external_stylesheets)\

app.title = 'Lifetime Earnings Comparison'

# Read data from an Excel file for both sheets
active_retire_df = pd.read_excel('mil_pay.xlsx', sheet_name='ActiveRetire')
reserve_retire_df = pd.read_excel('mil_pay.xlsx', sheet_name='ReserveRetire')

# Active retirement graph initial values
active_retire_default_start_year = active_retire_df['Military Pay'].diff().idxmin() + 1 if active_retire_df['Military Pay'].diff().idxmin() is not None else active_retire_df['Military Pay'].last_valid_index() + 1
active_retire_default_salary= active_retire_df['Military Pay'].max() if active_retire_df['Military Pay'].max() is not None else 80000
active_retire_default_end_year = active_retire_df['Gov\'t TSP Payout'].first_valid_index() - 1

# Reserve retirement graph initial values
reserve_retire_default_start_year = reserve_retire_df['Military Pay'].diff().idxmin() + 1 if reserve_retire_df['Military Pay'].diff().idxmin() is not None else reserve_retire_df['Military Pay'].last_valid_index() + 1
reserve_retire_default_salary= reserve_retire_df['Military Pay'].max() if reserve_retire_df['Military Pay'].max() is not None else 80000
reserve_retire_default_end_year = reserve_retire_df['Gov\'t TSP Payout'].first_valid_index() - 1

# Define the columns to be included in the visualization
active_retire_selected_columns = ['Military Pay', 'Bonus & Payments', 'BRS Pension', 'Service Member TSP Payout', "Gov't TSP Payout", 'Post Mil Retirement Pay']
reserve_retire_selected_columns = ['Military Pay', 'Bonus & Payments', 'BRS Pension', 'Service Member TSP Payout', "Gov't TSP Payout", 'Post Active Duty Pay']

# Define the layout of the app
app.layout = html.Div([
    html.H1("Active and Reserve Retirement Lifetime Earnings Comparison"),

    # Active retirement graph options
    html.Div([
    html.Label('Active retirement graph post-military retirement pay options: '),

    html.Div([
        html.Label('Civilian salary start year: ', style={'display': 'inline-block', 'width': '200px'}),
        dcc.Input(id='active_retire_start_year_input', type='number', value=active_retire_default_start_year),
    ]),

    html.Div([
        html.Label('Salary: ', style={'display': 'inline-block', 'width': '200px'}),
        dcc.Input(id='active_retire_salary_input', type='number', value=active_retire_default_salary),
    ]),

    html.Div([
        html.Label('Percent yearly raise: ', style={'display': 'inline-block', 'width': '200px'}),
        dcc.Input(id='active_retire_yearly_raise_input', type='number', value=0),
    ]),

    html.Div([
        html.Label('Civilian retirement: ', style={'display': 'inline-block', 'width': '200px'}),
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
        html.Label('Civilian salary start year: ', style={'display': 'inline-block', 'width': '200px'}),
        dcc.Input(id='reserve_retire_start_year_input', type='number', value=reserve_retire_default_start_year),
    ]),

    html.Div([
        html.Label('Salary: ', style={'display': 'inline-block', 'width': '200px'}),
        dcc.Input(id='reserve_retire_salary_input', type='number', value=reserve_retire_default_salary),
    ]),

    html.Div([
        html.Label('Percent yearly raise: ', style={'display': 'inline-block', 'width': '200px'}),
        dcc.Input(id='reserve_retire_yearly_raise_input', type='number', value=0),
    ]),

    html.Div([
        html.Label('End year: ', style={'display': 'inline-block', 'width': '200px'}),
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
     Input('active_retire_salary_input', 'value'),
     Input('active_retire_yearly_raise_input', 'value'),
     Input('active_retire_end_year_input', 'value')]
)
def update_active_retire_graph(start_year, salary, yearly_raise, end_year):
    active_retire_df['Post Mil Retirement Pay'] = 0

    try:
        start_year = int(start_year)
        start_year = max(0, min(start_year, active_retire_df['Calendar Year'].max()))
    except (ValueError, TypeError):
        raise PreventUpdate
    
    try:
        end_year = int(end_year)
        end_year = max(0, min(end_year, active_retire_df['Calendar Year'].max()))
    except (ValueError, TypeError):
        raise PreventUpdate
    
    try:
        salary= float(salary)
    except (ValueError, TypeError):
        raise PreventUpdate
    
    try:
        yearly_raise = float(yearly_raise) / 100.0
    except (ValueError, TypeError):
        raise PreventUpdate
    
    for year in range(start_year, end_year + 1):
        active_retire_df.loc[year, 'Post Mil Retirement Pay'] = salary
        salary *= (1 + yearly_raise)

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
     Input('reserve_retire_salary_input', 'value'),
     Input('reserve_retire_yearly_raise_input', 'value'),
     Input('reserve_retire_end_year_input', 'value')]
)
def update_reserve_retire_graph(start_year, salary, yearly_raise, end_year):
    try:
        start_year = int(start_year)
        start_year = max(0, min(start_year, reserve_retire_df['Calendar Year'].max()))
    except (ValueError, TypeError):
        raise PreventUpdate
    
    try:
        end_year = int(end_year)
        end_year = max(0, min(end_year, reserve_retire_df['Calendar Year'].max()))
    except (ValueError, TypeError):
        raise PreventUpdate

    try:
        salary = float(salary)
    except (ValueError, TypeError):
        raise PreventUpdate

    try:
        yearly_raise = float(yearly_raise) / 100.0
    except (ValueError, TypeError):
        raise PreventUpdate
    
    reserve_retire_df['Post Active Duty Pay'] = 0

    for year in range(start_year, end_year + 1):
        reserve_retire_df.loc[year, 'Post Active Duty Pay'] = salary
        salary *= (1 + yearly_raise)

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
