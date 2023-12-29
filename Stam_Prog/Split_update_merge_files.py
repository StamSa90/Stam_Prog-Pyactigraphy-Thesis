# Open function to open the file "MyFile1.txt"
# (same directory) in append mode and
import csv
from datetime import datetime
import sqlite3
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_regions(post_id):
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM regions WHERE Sleep_Wake is not null  and Interval_Status is not null and read_excel_id = ?',
                        (post_id,)).fetchall()
    conn.close()
    if posts is None:
        abort(404)
    return posts



def Split_file_for_Update(title):
         # Asks for search criteria from user
         #search_parts = input("Enter search criteria:\n").split(",")
         search_parts = ("Sleep/Wake"+",").split(",")
         # Opens csv data file
         print("file:"+ "./data/"+title)
         file = csv.reader(open("./data/"+title))

         # Go over each row and print it if it contains user input.
         row_num_header=0
         for row in file:
            row_num_header= row_num_header+1
            if all([x in row for x in search_parts]):
               
               # print("i="+str(i))
               break
         
         file1 = open("./data/"+title,"r")
         # store its reference in the variable file1
         # and "MyFile2.txt" in D:\Text in file2
   
         file2 = open(r"./data/"+title.replace('.csv','')+"1.csv","w+")
         file3 = open(r"./data/"+title.replace('.csv','')+"2.csv","w+")
         cur_row = 0
         for row in file1:
           
            cur_row = cur_row+1
            if cur_row < row_num_header:
               
               file2.writelines(row)
            else: 
               file3.writelines(row)
            file2.close
            file3.close

def Replace_Files(title,from_dt,to_dt,Sleep_Wake,Interval_Status):
      # open the file in read mode
      op = open('./data/'+title.replace('.csv','')+'2.csv', 'r')
      headers = ["Line","Date","Time","Off-Wrist Status","Activity","Marker","White Light","Red Light","Green Light","Blue Light","Sleep/Wake","Interval Status",]
      # creating dictreader object
      file = csv.DictReader(op)
      
      # creating empty lists
      records = []
      up_dt = []
      
      # iterating over each row and append

      for col in file:
         dt = str(col['Date']) + " "+str(col['Time'])
         #print(dt)
         datetime_object = datetime.strptime(dt, '%d/%m/%Y %H:%M:%S')
         # ελεγχει το ευρος των τιμων μας 
         if datetime_object >= datetime.strptime(from_dt, '%Y-%m-%d %H:%M:%S') and datetime_object <= datetime.strptime(to_dt, '%Y-%m-%d %H:%M:%S'):
         
            # row = {'Line':col["Line"],'Date':col["Date"],"Time":col["Time"],"Off-Wrist Status":col["Off-Wrist Status"],"Activity":col["Activity"],"Marker":col["Marker"],"White Light":col["White Light"],"Red Light":col["Red Light"],"Green Light":col["Green Light"],"Blue Light":col["Blue Light"],"Sleep/Wake":Sleep_Wake,"Interval Status":Interval_Status,}
            row = [col["Line"],col["Date"],col["Time"],col["Off-Wrist Status"],col["Activity"], col["Marker"],col["White Light"],col["Red Light"],col["Green Light"],col["Blue Light"],Sleep_Wake,Interval_Status,]
      
            up_dt.append(row)   
            records.append(col["Line"])  
         else:
            #row = {'Line':col["Line"],'Date':col["Date"],"Time":col["Time"],"Off-Wrist Status":col["Off-Wrist Status"],"Activity":col["Activity"],"Marker":col["Marker"],"White Light":col["White Light"],"Red Light":col["Red Light"],"Green Light":col["Green Light"],"Blue Light":col["Blue Light"],"Sleep/Wake":col["Sleep/Wake"],"Interval Status":col["Interval Status"],}
            row = [col["Line"],col["Date"],col["Time"],col["Off-Wrist Status"],col["Activity"], col["Marker"],col["White Light"],col["Red Light"],col["Green Light"],col["Blue Light"],col["Sleep/Wake"],col["Interval Status"],]
      
            up_dt.append(row)
      op.close()

      # update exam2.csv
      with open('./data/'+title.replace('.csv','')+'2.csv', 'wt',newline='') as f:
         csv_writer = csv.writer(f, quoting=csv.QUOTE_ALL)
         csv_writer.writerow(headers) # write header
         csv_writer.writerows(up_dt)
      # print("Update Lines :"+str(records))z
     
def  merge_two_csv_file(title):

      # merge_two_csv_file

      file_paths = [title.replace('.csv','')+'1.csv', title.replace('.csv','')+'2.csv']

      with open('./data/'+title.replace('.csv','')+'_upd.csv', 'w', encoding='utf-8') as output_file:
         for file_path in file_paths:
            with open("./data/"+file_path, 'r', encoding='utf-8') as input_file:
                  for line in input_file:
                     output_file.write(line)   

def Update_for_all_from_selector(excel_id,title,title_selector):
      posts = get_regions(excel_id)

     # Csv_file = open("./tmp/"+title_selector, 'r', encoding='utf-8') 
     # rows = csv.DictReader(Csv_file)
      for line in posts:
          Replace_Files(title,line['Start_Date'],line['End_Date'],line['Sleep_Wake'],line['Interval_Status'])
                       
def  Make_New_File_With_Selectors(excel_id,title,title_selector):
     print(title)
     print(title_selector)
     print('Split_file_for_Update(title)')
     Split_file_for_Update(title)
     print('Update_for_all_from_selector(excel_id,title,title_selector)')
     Update_for_all_from_selector(excel_id,title,title_selector)
     print('merge_two_csv_file(title)')
     merge_two_csv_file(title)
     print('after merge_two_csv_file(title)')