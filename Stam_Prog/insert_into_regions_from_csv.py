# importing csv module
import csv
# importing sqlite3 module
import sqlite3

def insert_regions_from_csv(csv_file_name):
    # read the csv file
    with open('./data/'+csv_file_name , 'r') as csvfile:
        # create the object of csv.reader()
        csv_file_reader = csv.reader(csvfile,delimiter=',')
        # skip the header 
        next(csv_file_reader,None)
                
        ##### create a database table using sqlite3###
        
              
        # 2. create database
        connection=sqlite3.connect('database.db')
        curosr=connection.cursor()
           

        # 4. pase csv data
        for row in csv_file_reader:
            # skip the first row
            for i in range(len(row)):
                # assign each field its value
                read_excel_id=row[0]
                start_date=row[1]
                end_date=row[2]
                
            
            # 5. create insert query
            InsertQuery=f"INSERT INTO regions (read_excel_id,start_date,end_date) VALUES ('{read_excel_id}','{start_date}','{end_date}')"
            # 6. Execute query
            curosr.execute(InsertQuery)
        # 7. commit changes
        connection.commit()
        # 8. close connection
        connection.close()