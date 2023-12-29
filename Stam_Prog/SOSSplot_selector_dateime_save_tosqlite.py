import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

# Sample data with datetime values
data = {
    'Datetime': pd.date_range(start='2023-01-01', periods=100, freq='H'),
    'Value': [10 + i for i in range(100)]
}

df = pd.DataFrame(data)

# Initialize the SQLite3 database
conn = sqlite3.connect('datetime_data.db',check_same_thread=False)
cursor = conn.cursor()

# Create a table to store max and min datetime values
cursor.execute('''CREATE TABLE IF NOT EXISTS datetime_range (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  max_datetime DATETIME,
                  min_datetime DATETIME)''')
conn.commit()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    dcc.Graph(
        id='scatter-plot',
        config={'editable': True},
        figure=px.scatter(df, x='Datetime', y='Value', title='Select Datetime Range to Get Max and Min'),
    ),
    html.Div(id='selected-data-output'),
])

# Define callback function to get max and min datetime values and save to SQLite3
@app.callback(
    Output('selected-data-output', 'children'),
    Input('scatter-plot', 'selectedData')
)
def display_selected_data(selectedData):
    if selectedData is not None:
        x_values = [pd.to_datetime(point['x']) for point in selectedData['points']]
        if x_values:
            max_datetime = max(x_values)
            min_datetime = min(x_values)
            max_datetime_str = max_datetime.strftime('%Y-%m-%d %H:%M:%S')
            min_datetime_str = min_datetime.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO datetime_range (max_datetime, min_datetime) VALUES (?, ?)",
                           (max_datetime_str, min_datetime_str))
            conn.commit()
            return f"Selected Datetime Range: Max Datetime={max_datetime_str}, Min Datetime={min_datetime_str} (Saved to SQLite3)"
        else:
            return "No datetime range selected."
    else:
        return "No data points selected."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
