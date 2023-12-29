import dash
from dash import dcc, html, Input, Output

import plotly.express as px
import pandas as pd
import sqlite3
import csv
from dash import dash_table

import  openAnActygrafy  as  oa

def Make_Selection(File_Formats,file,read_excel_id):
    raw = oa.open_file(File_Formats,file) 
    Selector_raw(raw,read_excel_id)

def Selector_raw(raw,read_excel_id):
    app = dash.Dash(__name__)
    sadeh = raw.Sadeh()
    scripps = raw.Scripps()
    CK = raw.CK()
    excel_id = read_excel_id

    # Sample data with datetime values
    data = {
    'Datetime': raw.data.index.astype(str),
    'Value': raw.data
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
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS  regions (
                        id	INTEGER NOT NULL,
                        read_excel_id	INTEGER NOT NULL,
                        new_excel_id	INTEGER,
                        start_date	TEXT NOT NULL,
                        end_date	TEXT NOT NULL,
                        Sleep_Wake	TEXT,
                        Interval_Status	TEXT,
                        PRIMARY KEY("id" AUTOINCREMENT)
                    )''')

    conn.commit()



    # Define the app layout
    app.layout = html.Div([
    dcc.Graph(
        id='scatter-plot',
        config={'editable': True},
        figure=px.scatter(df, x='Datetime', y='Value', title='Select Datetime Range to Get Max and Min'),
    ),
    html.Div(id='selected-data-output'),
    html.Hr(),  # Horizontal line separator
    html.H3("Data from Database"),
    dash_table.DataTable(
        id='database-data-table',
        columns=[
            {'name': 'ID', 'id': 'id'},
            {'name': 'read_excel_id', 'id': 'read_excel_id'},
            {'name': 'new_excel_id', 'id': 'new_excel_id'},
            {'name': 'start_date', 'id': 'start_date'},
            {'name': 'end_date', 'id': 'end_date'},
            {'name': 'Sleep_Wake', 'id': 'Sleep_Wake'},
            {'name': 'Interval_Status', 'id': 'Interval_Status'},
            
        ],
        data=[],  # Empty data to be filled by the callback
    )
    ])

    # Define callback function to get max and min datetime values and save to SQLite3 and CSV
    @app.callback(
    [Output('selected-data-output', 'children'),
     Output('database-data-table', 'data')],
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
                        
                        # Save to SQLite3
                        cursor.execute("INSERT INTO regions (read_excel_id, start_date,end_date) VALUES (?,?,?)",
                                        (excel_id, min_datetime_str,max_datetime_str,))
                        conn.commit()
                        
                        # Save to CSV
                        with open('datetime_data.csv', mode='a', newline='') as csv_file:
                            csv_writer = csv.writer(csv_file)
                            csv_writer.writerow([max_datetime_str, min_datetime_str])
                        
                        # Fetch data from the database and display it in the table
                        cursor.execute("SELECT * FROM regions")
                        database_data = cursor.fetchall()
                        table_data = [{'id': row[0], 'read_excel_id':row[1], 'new_excel_id':row[2],'start_date': row[3], 'end_date': row[4]} for row in database_data]
                        
                        return (f"Selected Datetime Range: end_date={max_datetime_str}, start_date={min_datetime_str} "
                                f"(Saved to SQLite3 and CSV)"), table_data
                    else:
                        return "No datetime range selected.", []
                else:
                    return "No data points selected.", []
               # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)


 