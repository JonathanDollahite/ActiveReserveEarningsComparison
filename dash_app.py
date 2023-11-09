# Import necessary libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output

# Create a Dash application
app = Dash(__name__)

# Read data from an Excel file
mil_pay_df = pd.read_excel('mil_pay.xlsx')

# Calculate the last valid index of 'Military Pay' column
last_year_active = mil_pay_df['Military Pay'].last_valid_index()

# Define the number of years to consider for post-military retirement pay
years, n = mil_pay_df['Calendar Year'], 20

# Initialize a new column 'Post Mil Retirement Pay' with zeros
mil_pay_df['Post Mil Retirement Pay'] = [0] * len(years)

# Set a fixed value of 123,000 for post-military retirement pay for a certain range of years
if last_year_active is not None:
    mil_pay_df.loc[last_year_active + 1:last_year_active + n, 'Post Mil Retirement Pay'] = 123000

# Define the columns to be included in the visualization
selected_columns = ['Military Pay', 'Bonus & Payments', 'BRS Pension', 'Service Member TSP Payout', "Gov't TSP Payout", 'Post Mil Retirement Pay']

# Define the layout of the app
app.layout = html.Div([
    html.H1("Military Pay Data Visualization"),
    
    # Create a Graph component with an ID
    dcc.Graph(id='military-pay-graph'),
    
    # Dummy input element that doesn't affect the layout
    dcc.Input(id='dummy-input', style={'display': 'none'}, value='')
])

# Create a callback function to update the graph
@app.callback(
    Output('military-pay-graph', 'figure'),
    [Input('dummy-input', 'value')]
)
def update_graph(value):
    # Initialize an empty list to store the data traces for the graph
    data = []

    # Create a bar trace for each selected column
    for column in selected_columns:
        trace = go.Bar(
            x=mil_pay_df['Calendar Year'],
            y=mil_pay_df[column],
            name=column
        )
        data.append(trace)

    # Define the layout for the graph
    layout = go.Layout(
        barmode='stack',  # Stack bars on top of each other
        title='Military Pay Data'  # Set the title for the graph
    )

    # Create a figure with the data and layout
    fig = go.Figure(data=data, layout=layout)
    
    return fig

# Run the app if this script is the main entry point
if __name__ == '__main__':
    app.run_server(debug=True)
