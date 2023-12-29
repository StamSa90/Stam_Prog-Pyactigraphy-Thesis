import dash
from dash import dcc,  Input, Output
from dash import html
import plotly.express as px
import pandas as pd
import sqlite3
import csv
from dash import dash_table
import Py_actigrafi_app as Py
from collections import OrderedDict
from dash.dependencies import Input, Output, State
def get_data1(pserver,p_File_Formats,p_file,p_folder):

    raw = Py.open_file(p_File_Formats,p_folder,p_file)
    print(raw)
    # Sample data with datetime values
    
    #data = { 
   #     'Datetime': pd.date_range(start='2023-01-01', periods=100, freq='H'),
    #    'Value': [10 + i for i in range(100)]
   # }
    data = {
        'Datetime': raw.data.index.astype(str),
        'Value': raw.data
    }
   

    df = pd.DataFrame(data)
    df1 = pd.DataFrame(OrderedDict([
     ('Interval_Status', ['ACTIVE', 'REST-S', 'REST','STAM'])
      
    ]))
    df2 = pd.DataFrame(OrderedDict([
        ('Sleep_Wake',['0','1','9'])
    ]))
    #print(df)
    # Initialize the SQLite3 database
    conn = sqlite3.connect('database.db',check_same_thread=False)
    cursor = conn.cursor()

    # Create a table to store max and min datetime values
    cursor.execute('''CREATE TABLE IF NOT EXISTS regions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    read_excel_id TEXT,
                    new_excel_id  TEXT,
                    start_date DATETIME,
                    end_date DATETIME,
                    Sleep_Wake TEXT,
                    Interval_Status TEXT)''')
    conn.commit()

    # Initialize the Dash app
   # app = dash.Dash(__name__)
    external_stylesheets = ['styles.css']
    app = dash.Dash(__name__, server=pserver, url_base_pathname='/dash_interval/', external_stylesheets=external_stylesheets)
   # print("ffffffffffffffffffffffffffffffffff")
    # Define external CSS file for styling
    
 
    # Define the app layout
    app.layout = html.Div([
        dcc.Graph(
            id='scatter-plot',
            config={'editable': True},
            figure=px.scatter(df, x='Datetime', y='Value', title='Select Datetime Range to Get Min  and Max From Actigraphy data'),
        ),
        html.Div(id='selected-data-output'),
        html.Hr(),  # Horizontal line separator
        html.H3("Data from Database"),
        html.Button('Save to CSV', id='save-button'),
        dash_table.DataTable(
            id='database-data-table',
            columns=[
                {'name': 'ID', 'id': 'id'},
                {'name': 'read_excel_id', 'id': 'read_excel_id'},
                {'name': 'new_excel_id', 'id': 'new_excel_id'},
                {'name': 'start_date', 'id': 'start_date'},
                {'name': 'end_date', 'id': 'end_date'},
                {'name': 'Sleep_Wake', 'id': 'Sleep_Wake', 'presentation': 'dropdown'},
                {'name': 'Interval_Status', 'id': 'Interval_Status', 'presentation': 'dropdown'},
               
                
            ],
            data=[],  # Empty data to be filled by the callback
            editable=True,
            row_deletable=True,
            dropdown={         
            'Interval_Status': {
                 'options': [
                    {'label': i, 'value': i}
                    for i in df1['Interval_Status'].unique()
                ]
            },
            'Sleep_Wake': {
                 'options': [
                    {'label': i, 'value': i}
                    for i in df2['Sleep_Wake'].unique()
                ]
            }

        }
        ),html.Div(id='table-dropdown-container')
         ,html.Div(id='output-container')
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
                end_date = max(x_values)
                start_date = min(x_values)
                end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')
                start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
                
                # Save to SQLite3
                cursor.execute("INSERT INTO regions (read_excel_id,new_excel_id,Sleep_Wake,Interval_Status,start_date,end_date) VALUES (?,?,?,?,?,?)",
                            ('78','','','',start_date_str,end_date_str))
                conn.commit()
                
                # Save to CSV
                with open('datetime_data.csv', mode='a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([ start_date_str,end_date_str])
                
                # Fetch data from the database and display it in the table
                cursor.execute("SELECT * FROM regions")
                database_data = cursor.fetchall()
                table_data = [{'id': row[0], 'read_excel_id': row[1],'new_excel_id':row[2], 'start_date': row[3] ,'end_date': row[4], 'Sleep_Wake': row[5], 'Interval_Status': row[6], } for row in database_data]
                
                return (f"Selected Datetime Range: Min Datetime={start_date_str} , Max Datetime={end_date_str} "
                        f"(Saved to SQLite3 and CSV)"), table_data
            else:
                return "No datetime range selected.", []
        else:
            cursor.execute("SELECT * FROM regions")
            database_data = cursor.fetchall()
            table_data = [{'id': row[0], 'read_excel_id': row[1],'new_excel_id':row[2], 'start_date': row[3] ,'end_date': row[4], 'Sleep_Wake': row[5], 'Interval_Status': row[6], } for row in database_data]
            return (f"(No data points selected.)"), table_data
    
    @app.callback(
    Output('output-container', 'children'),
    [Input('save-button', 'n_clicks')],
    [State('database-data-table', 'data')]
    )
    def save_to_csv(n_clicks, table_data):

        if n_clicks is None:
            return "Click the 'Save to CSV' button."

        # Convert the table data to a DataFrame
        df = pd.DataFrame(table_data)

        # Specify the CSV file path
        csv_file_path = 'datetime_data.csv'

        # Save the DataFrame to a CSV file
        df.to_csv(csv_file_path, index=False,quoting=csv.QUOTE_ALL)
        conn.commit()
        cursor.execute('DELETE FROM regions')
        for row in table_data :
           
          #print(row)
          #print(row['id'])
           
           
           cursor.execute("INSERT INTO regions (id,read_excel_id,Sleep_Wake,Interval_Status,start_date,end_date) VALUES (?,?,?,?,?,?)",
                     ( row['id'], row['read_excel_id'], row['Sleep_Wake'], row['Interval_Status'] ,row['start_date'],row['end_date']))
           conn.commit()   
        
        return f'Data saved to {csv_file_path}.'

     
    # Run the app
    if __name__ == '__main__':
       app.run_server(debug=True)
       # app.run_server()

#p_File_Formats = 'rpx'
#p_file = 'example.csv'
#p_folder = 'data/'

#get_data1(p_File_Formats,p_file,p_folder)