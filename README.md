# ActiveReserveEarningsComparison

This code sets up a Dash web application to compare the lifetime pay of active and reserve military personnel after retirement. It uses the Plotly library for graph visualization and the Dash framework for creating interactive web applications. The data is read from an Excel file with two sheets: 'ActiveRetire' and 'ReserveRetire'. The initial values for the graphs are set based on certain calculations from the data.

The Dash app layout consists of two sections, one for active retirement and the other for reserve retirement. Each section includes input fields for start year, amount, and end year, allowing users to customize the visualization. The graphs are updated dynamically using callback functions that respond to changes in input values. The active retirement graph displays various components of military pay over time, and the same applies to the reserve retirement graph.

Callbacks modify the data based on user inputs and update the corresponding graphs. The application can be run as a standalone script, and when executed, it launches a server, making the app accessible through a web browser.
