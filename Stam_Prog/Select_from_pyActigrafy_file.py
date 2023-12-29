import dash
from dash import dcc,  Input, Output
from dash import html
import plotly.express as px
import pandas as pd
import sqlite3
import csv
from dash import dash_table
import Py_actigrafi_app as Py
from flask import Flask, Blueprint
from collections import OrderedDict
from dash.dependencies import Input, Output, State


def get_data1(pserver,p_File_Formats,p_file,p_folder):

    raw = Py.open_file(p_File_Formats,p_folder,p_file)
   # print(raw)
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
     ('TYPE', ['NIGHT', 'NAP', 'NOWEAR'])
    ]))
    #print(df)
    # Initialize the SQLite3 database
    conn = sqlite3.connect('database.db',check_same_thread=False)
    cursor = conn.cursor()

    # Create a table to store max and min datetime values
    cursor.execute('''CREATE TABLE IF NOT EXISTS datetime_range (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    TYPE TEXT,
                    START DATETIME,
                    END DATETIME)''')
    conn.commit()

    # Initialize the Dash app
   # app = dash.Dash(__name__)
    external_stylesheets = ['styles.css']
    app = dash.Dash(__name__, server=pserver, url_base_pathname='/dash/', external_stylesheets=external_stylesheets)
    
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
                {'name': 'Type', 'id': 'TYPE', 'presentation': 'dropdown'},
                {'name': 'Min Datetime', 'id': 'START'},
                {'name': 'Max Datetime', 'id': 'END'},
                
            ],
            data=[],  # Empty data to be filled by the callback
            editable=True,
            row_deletable=True,
            dropdown={         
            'TYPE': {
                 'options': [
                    {'label': i, 'value': i}
                    for i in df1['TYPE'].unique()
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
                max_datetime = max(x_values)
                min_datetime = min(x_values)
                max_datetime_str = max_datetime.strftime('%Y-%m-%d %H:%M:%S')
                min_datetime_str = min_datetime.strftime('%Y-%m-%d %H:%M:%S')
                
                # Save to SQLite3
                cursor.execute("INSERT INTO datetime_range (TYPE,START,END) VALUES (?, ?,?)",
                            ('',min_datetime_str,max_datetime_str))
                conn.commit()
                
                # Save to CSV
                with open('2Selected_data.csv', mode='a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([ min_datetime_str,max_datetime_str])
                
                # Fetch data from the database and display it in the table
                cursor.execute("SELECT * FROM datetime_range")
                database_data = cursor.fetchall()
                table_data = [{'id': row[0], 'TYPE': row[1], 'START': row[2] ,'END': row[3], } for row in database_data]
                
                return (f"Selected Datetime Range: Min Datetime={min_datetime_str} , Max Datetime={max_datetime_str} "
                        f"(Saved to SQLite3 and CSV)"), table_data
            else:
                return "No datetime range selected.", []
        else:
            cursor.execute("SELECT * FROM datetime_range")
            database_data = cursor.fetchall()
            table_data = [{'id': row[0], 'TYPE': row[1], 'START': row[2] ,'END': row[3], } for row in database_data]
            
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

        hed_data = [ {'SUBJECT ID':" ", 'EXAMPLE_01':" "," " :" "," ":" "," ":" " }]
        df1 = pd.DataFrame(hed_data)

        df1.to_csv('1header.csv', index=False,quoting=csv.QUOTE_ALL)
       
        df = pd.DataFrame(table_data)
        
        column_to_exclude = 'id'

        new_df = df.drop(columns=[column_to_exclude])
        
        new_df["DURATION (min)"] = ""
        new_df[""] = ""
        
          
        
              # Specify the CSV file path
        csv_file_path = '2Selected_data.csv'
       
        # Specify the paths of the two files
        file1_path = '1header.csv'
        file2_path = '2Selected_data.csv'
        output_file_path = './data/example_01_sleepdiary.csv'

        # Read data from the first file
        with open(file1_path, 'r') as file1:
            data_file1 = file1.read()

        # Read data from the second file
        with open(file2_path, 'r') as file2:
            data_file2 = file2.read()

        # Combine the data
        combined_data = data_file1 + data_file2

        # Write the combined data to a new file
        with open(output_file_path, 'w') as output_file:
            output_file.write(combined_data)




        
        # Save the DataFrame to a CSV file
        new_df.to_csv(csv_file_path, index=False,quoting=csv.QUOTE_ALL)


        
        cursor.execute('DELETE FROM datetime_range')
        conn.commit()
        for row in table_data :
           
          #print(row)
          #print(row['id'])
           
           
           cursor.execute("INSERT INTO datetime_range (id,TYPE,START,END) VALUES (?,?,?,?)",
                     ( row['id'], row['TYPE'] ,row['START'],row['END']))
           conn.commit()   
        
        return f'Data saved to {csv_file_path}.'

     
    # Run the app
    if __name__ == '__main__':
       app.run_server()
       # app.run_server()

#p_File_Formats = 'rpx'
#p_file = 'example.csv'
#p_folder = 'data/'

#get_data1(p_File_Formats,p_file,p_folder)