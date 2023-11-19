# Import necessary libraries
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
from dash.exceptions import PreventUpdate

# Set the style for the page
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Create a Dash application
app = Dash(__name__, external_stylesheets=external_stylesheets)\

server = app.server

app.title = 'Active vs Reserve Lifetime Earnings Comparison'

# Read data from an Excel file for both sheets
active_df = pd.read_excel('mil_pay.xlsx', sheet_name='ActiveRetire')
reserve_df = pd.read_excel('mil_pay.xlsx', sheet_name='ReserveRetire')

# Active retirement graph initial values
active_default_start_year = active_df['Military Pay'].diff().idxmin() + 1 if active_df['Military Pay'].diff().idxmin() is not None else active_df['Military Pay'].last_valid_index() + 1
active_default_salary= active_df['Military Pay'].max() if active_df['Military Pay'].max() is not None else 80000
active_default_end_year = active_df['Gov\'t TSP Payout'].first_valid_index() - 1

# Reserve retirement graph initial values
reserve_default_start_year = reserve_df['Military Pay'].diff().idxmin() + 1 if reserve_df['Military Pay'].diff().idxmin() is not None else reserve_df['Military Pay'].last_valid_index() + 1
reserve_default_salary= reserve_df['Military Pay'].max() if reserve_df['Military Pay'].max() is not None else 80000
reserve_default_end_year = reserve_df['Gov\'t TSP Payout'].first_valid_index() - 1

# Define the columns to be included in the visualization
selected_columns = ['Military Pay', 'Bonus & Payments', 'BRS Pension', 'Service Member TSP Payout', "Gov't TSP Payout", 'Post Active Duty Pay']
active_df['Post Active Duty Pay'] = 0
reserve_df['Post Active Duty Pay'] = 0
    
# Define the layout of the app
app.layout = html.Div([
    html.H1("Active vs Reserve Lifetime Earnings Comparison"),

    html.Div([

        # Active retirement graph options
        html.Div([
        html.Label('Active retirement graph post-military retirement pay options: '),

        html.Div([
            html.Label('Civilian salary start year: ', style={'display': 'inline-block', 'width': '200px'}),
            dcc.Input(id='active_start_year_input', type='number', value=active_default_start_year),
        ]),

        html.Div([
            html.Label('Salary: ', style={'display': 'inline-block', 'width': '200px'}),
            dcc.Input(id='active_salary_input', type='number', value=active_default_salary),
        ]),

        html.Div([
            html.Label('Percent yearly raise: ', style={'display': 'inline-block', 'width': '200px'}),
            dcc.Input(id='active_yearly_raise_input', type='number', value=0),
        ]),

        html.Div([
            html.Label('Civilian retirement: ', style={'display': 'inline-block', 'width': '200px'}),
            dcc.Input(id='active_end_year_input', type='number', value=active_default_end_year),
        ]),

        html.Div(id='active_lifetime_earnings'),

        ], style={'width': '48%', 'float': 'left', 'margin-right': '2%'}),


    # Reserve retirement graph options
    html.Div([
        html.Label('Reserve retirement graph post-active duty pay options: '),

        html.Div([
            html.Label('Civilian salary start year: ', style={'display': 'inline-block', 'width': '200px'}),
            dcc.Input(id='reserve_start_year_input', type='number', value=reserve_default_start_year),
        ]),

        html.Div([
            html.Label('Salary: ', style={'display': 'inline-block', 'width': '200px'}),
            dcc.Input(id='reserve_salary_input', type='number', value=reserve_default_salary),
        ]),

        html.Div([
            html.Label('Percent yearly raise: ', style={'display': 'inline-block', 'width': '200px'}),
            dcc.Input(id='reserve_yearly_raise_input', type='number', value=0),
        ]),

        html.Div([
            html.Label('End year: ', style={'display': 'inline-block', 'width': '200px'}),
            dcc.Input(id='reserve_end_year_input', type='number', value=reserve_default_end_year),
        ]),

        html.Div(id='reserve_lifetime_earnings'),

        ], style={'width': '48%', 'float': 'right'}),
    ]),


    html.Div([
        # Active retirement graph
        dcc.Graph(id='active_graph'),
    ], style={'width': '48%', 'float': 'left', 'margin-right': '2%'}),

    html.Div([
        # Reserve retirement graph
        dcc.Graph(id='reserve_graph'),
    ], style={'width': '48%', 'float': 'right'}),
])


# Create a single callback function to update both graphs
@app.callback(
    [
        Output('active_graph', 'figure'),
        Output('active_lifetime_earnings', 'children'),
        Output('reserve_graph', 'figure'),
        Output('reserve_lifetime_earnings', 'children')
    ],
    [
        Input('active_start_year_input', 'value'),
        Input('active_salary_input', 'value'),
        Input('active_yearly_raise_input', 'value'),
        Input('active_end_year_input', 'value'),
        Input('reserve_start_year_input', 'value'),
        Input('reserve_salary_input', 'value'),
        Input('reserve_yearly_raise_input', 'value'),
        Input('reserve_end_year_input', 'value')
    ]
)
def update_graphs(
        active_start_year, active_salary, active_yearly_raise, active_end_year,
        reserve_start_year, reserve_salary, reserve_yearly_raise, reserve_end_year
):
    # Update active retirement graph
    active_fig, active_earnings_div = update_retire_graph(
        active_df, selected_columns,
        active_start_year, active_salary, active_yearly_raise, active_end_year
    )

    # Update reserve retirement graph
    reserve_fig, reserve_earnings_div = update_retire_graph(
        reserve_df, selected_columns,
        reserve_start_year, reserve_salary, reserve_yearly_raise, reserve_end_year
    )

    # Update active retirement graph
    active_fig, active_earnings_div = update_retire_graph(
        active_df, selected_columns,
        active_start_year, active_salary, active_yearly_raise, active_end_year
    )

    return active_fig, active_earnings_div, reserve_fig, reserve_earnings_div


def update_retire_graph(df, selected_columns, start_year, salary, yearly_raise, end_year):
    try:
        start_year = int(start_year)
        start_year = max(0, min(start_year, df['Calendar Year'].max()))
    except (ValueError, TypeError):
        raise PreventUpdate
    
    try:
        end_year = int(end_year)
        end_year = max(0, min(end_year, df['Calendar Year'].max()))
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

    df[selected_columns[-1]] = 0
    
    for year in range(start_year, end_year + 1):
        df.loc[year, selected_columns[-1]] = salary
        salary *= (1 + yearly_raise)

    data = []
    lifetime_earnings = 0

    for column in selected_columns:
        trace = go.Bar(
            x=df['Calendar Year'],
            y=df[column],
            name=column
        )
        data.append(trace)

        lifetime_earnings += df[column].sum()

    # Calculate max_value for both graphs
    max_value = max(active_df[selected_columns].sum(axis=1).max(),
                    reserve_df[selected_columns].sum(axis=1).max())
    
    # Determine max_yaxis_value based on the specified conditions
    max_yaxis_value = max(250000, int((max_value + 49999) / 50000) * 50000)

    # Set the y-axis range dynamically
    layout = go.Layout(
        barmode='stack',
        title='Retirement Graph',
        yaxis=dict(range=[0, max_yaxis_value])
    )

    fig = go.Figure(data=data, layout=layout)

    lifetime_earnings = "${:,.2f}".format(lifetime_earnings)

    lifetime_earnings_div = html.Div(
        children=[
            html.Div("Lifetime Earnings", style={'font-weight': 'bold'}),
            html.Div(lifetime_earnings, style={'border': '2px solid black', 'padding': '10px', 'width': '48%', 'float': 'left'})
        ]
    )

    return fig, lifetime_earnings_div


# Run the app if this script is the main entry point
if __name__ == '__main__':
    app.run_server(debug=True)
