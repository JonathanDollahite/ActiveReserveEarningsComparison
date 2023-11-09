# Import necessary libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output

# Create a Dash application
app = Dash(__name__)

# Read data from an Excel file for both sheets
active_retire_df = pd.read_excel('mil_pay.xlsx', sheet_name='ActiveRetire')
reserve_retire_df = pd.read_excel('mil_pay.xlsx', sheet_name='ReserveRetire')

# Define the number of years to consider for post-military retirement pay
years = active_retire_df['Calendar Year']
n = 20

# Initialize a new column 'Post Mil Retirement Pay' with zeros
active_retire_df['Post Mil Retirement Pay'] = [0] * len(years)
reserve_retire_df['Post Mil Retirement Pay'] = [0] * len(years)

# Calculate the last valid index of 'Military Pay' column for both sheets
last_year_active = active_retire_df['Military Pay'].last_valid_index()
last_year_reserve = reserve_retire_df['Military Pay'].last_valid_index()

# Set a fixed value of 123,000 for post-military retirement pay for a certain range of years for both sheets
if last_year_active is not None:
    active_retire_df.loc[last_year_active + 1:last_year_active + n, 'Post Mil Retirement Pay'] = 123000
if last_year_reserve is not None:
    reserve_retire_df.loc[last_year_reserve + 1:last_year_reserve + n, 'Post Mil Retirement Pay'] = 123000

# Define the columns to be included in the visualization
selected_columns = ['Military Pay', 'Bonus & Payments', 'BRS Pension', 'Service Member TSP Payout', "Gov't TSP Payout", 'Post Mil Retirement Pay']

# Define the layout of the app
app.layout = html.Div([
    html.H1("Military Pay Data Visualization"),
    
    # Create two Graph components with IDs
    dcc.Graph(id='active_retire_graph'),
    dcc.Graph(id='reserve_retire_graph'),
    
    # Dummy input elements that don't affect the layout
    dcc.Input(id='dummy_input_1', style={'display': 'none'}, value=''),
    dcc.Input(id='dummy_input_2', style={'display': 'none'}, value='')
])

# Create callback functions to update the graphs for ActiveRetire and ReserveRetire sheets
@app.callback(
    Output('active_retire_graph', 'figure'),
    [Input('dummy_input_1', 'value')]
)
def update_active_retire_graph(value):
    data = []

    for column in selected_columns:
        trace = go.Bar(
            x=years,
            y=active_retire_df[column],
            name=column
        )
        data.append(trace)

    layout = go.Layout(
        barmode='stack',
        title='Active Retirement Graph'
    )

    fig = go.Figure(data=data, layout=layout)
    
    return fig

@app.callback(
    Output('reserve_retire_graph', 'figure'),
    [Input('dummy_input_2', 'value')]
)
def update_reserve_retire_graph(value):
    data = []

    for column in selected_columns:
        trace = go.Bar(
            x=years,
            y=reserve_retire_df[column],
            name=column
        )
        data.append(trace)

    layout = go.Layout(
        barmode='stack',
        title='Reserve Retirement Graph'
    )

    fig = go.Figure(data=data, layout=layout)
    
    return fig

# Run the app if this script is the main entry point
if __name__ == '__main__':
    app.run_server(debug=True)