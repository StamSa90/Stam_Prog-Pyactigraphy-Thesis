import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect,current_app
import Py_actigrafi_app as Py
import Py_Actigrafy_day_by_day as Py_DBD
from werkzeug.exceptions import abort
import cp
import openAnActygrafy as oa
import main_Stam as ms
import Split_update_merge_files as Supmf
import insert_into_regions_from_csv as ins_reg
import main_Stam_Plot  as main_plot
import pandas as pd
from datetime import datetime
import Select_with_plotly as S_w_p
import Select_from_pyActigrafy_file as Selector
import Select_from_pyActigrafy_file_iterval as Selector_interval
from dash import Dash
from dash import html
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_region_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM regions WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_regions(post_id):
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM regions WHERE read_excel_id = ?',
                        (post_id,)).fetchall()
    conn.close()
    if posts is None:
        abort(404)
    return posts

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
p_File_Formats = 'rpx'
p_file = 'example.csv'
p_folder = 'data/'
Selector.get_data1(app,p_File_Formats,p_file,p_folder)
Selector_interval.get_data1(app,p_File_Formats,p_file,p_folder)


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

###################   post
@app.route('/<int:post_id>', methods=('GET', 'POST'))
def post(post_id):
    post = get_post(post_id)
   
    if request.method == 'POST':
       
        title = request.form['title']
        raw_start_time = request.form['raw_start_time']  
        raw_duration = request.form['raw_duration']   #period
        d_File_Formats = request.form['file_formats']
        d_folder = 'data/' 
        d_file =  title     
        d_start_time= raw_start_time  
        d_period = raw_duration
       
        if not title:
            flash('Title is required!')
        else:
            user1 = request.args.get('sid')
           
            button_clicked = request.form['button_clicked']
            if button_clicked == 'Button 1':
              
                Py.Data(d_File_Formats,d_folder,d_file)
            elif button_clicked == 'Button 2':
                print("Button 2")
                #S_w_p.Make_Selection(file_formats,'./tmp/'+title,post_id)
                Py.Daily_activity_profile(d_File_Formats,d_folder,d_file)
            elif button_clicked == 'Button 3':
                Py.Data_Masking(d_File_Formats,d_folder,d_file)
                print("Button 3")
            elif button_clicked == 'Button 4':
                
                Py.Cosinor_analysis(d_File_Formats,d_folder,d_file,d_start_time,d_period)
                print("Button 4")
            elif button_clicked == 'Button 5':
                Py.Functional_linear_modelling(d_File_Formats,d_folder,d_file,d_start_time,d_period)
                print("Button 5")
            elif button_clicked == 'Button 6':
                Py.Cleaning_files_individually(d_File_Formats,d_folder,d_file,d_start_time,d_period)
                print("Button 6")
            elif button_clicked == 'Button 7':
                Py.Roennebergs_algorithm (d_File_Formats,d_folder,d_file)
                print("Button 7")
            elif button_clicked == 'Button 8':
                Py.Singular_spectrum_analysis(d_folder,d_File_Formats,d_file,d_start_time,d_period)
                print("Button 8")
            elif button_clicked == 'Button 9':
                Py.Multi_fractal(d_folder,d_file,d_start_time,d_period)
                print("Button 9")
            elif button_clicked == 'Button 10':
                Py.Consolidated_activity_rest_period_detection(d_File_Formats,d_folder,d_file)
                print("Button 10")
            elif button_clicked == 'Button 11':
                d_sleep_diary_file = 'example_01_sleepdiary.csv'
                d_Add_custom_states_file ='example_01_sleepdiary_extra_states.csv'
                Py.Read_a_sleep_diary(d_File_Formats,d_folder,d_file,d_sleep_diary_file,d_Add_custom_states_file)
                print("Button 11")
            elif button_clicked == 'Button 12':
                Py.Automatic_detection_of_rest_activity_periods('data/','test_sample_rpx_eng.csv','2015-07-04 12:00:00','6 days','ENG_UK')
                print("Button 12")
            elif button_clicked == 'Button 13':
             #   Selector.get_data1(d_File_Formats,d_file,d_folder)    
                    print("Button 13")
                    return redirect(url_for('/dash/'))
            elif button_clicked == 'Button 15':
             #   Selector.get_data1(d_File_Formats,d_file,d_folder)    
                    print("Button 13")
                    return redirect(url_for('/dash_interval/'))
            elif button_clicked == 'Button 14':
                Py_DBD.Actigrafy_day_by_day(d_File_Formats,d_folder,d_file,d_start_time,d_period)
                print("Button 14")
       # return redirect(url_for('post'))
    return render_template('post.html', post=post)


@app.route('/crt', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        File_Formats = request.form['File_Formats']

        if not title:
            flash('Title is required!')
        elif not File_Formats:
            flash('File_Formats is required!')
            
        else:
             #print(content+title)
             cp.cp_files('c:/files/'+title,'./data/'+title);
           #  main.GetActigrafy('./tmp/'+title)
             raw = oa.open_file(File_Formats,'./data/'+title)
             raw.create_inactivity_mask(duration='2h00min')
             # oa.data_masking(raw)
             raw_name=raw.name
             raw_start_time=str(raw.start_time)
             raw_duration =str(raw.duration())
             raw_uuid = str(raw.uuid)
             raw_frequency=str(raw.frequency)
             raw_AonT=str(raw.AonT(freq='15min', binarize=True))
             raw_AoffT=str(raw.AoffT(freq='15min', binarize=True))
             raw_sleep_diary=str(raw.sleep_diary)
             conn = get_db_connection()
             conn.execute('INSERT INTO posts (title, content,raw_name,raw_start_time,raw_duration,raw_uuid,raw_frequency,raw_AonT,raw_AoffT,raw_sleep_diary,File_Formats) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                         (title, content,raw_name,raw_start_time,raw_duration,raw_uuid,raw_frequency,raw_AonT,raw_AoffT,raw_sleep_diary,File_Formats))
            
             conn.commit()
             conn.close()
             return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        
        id = request.form['id']
        created = request.form['created']
        title = request.form['title']
        content = request.form['content']
        raw_name = request.form['raw_name']
        raw_start_time = request.form['raw_start_time']
        raw_duration = request.form['raw_duration']
        raw_uuid = request.form['raw_uuid']
        raw_frequency = request.form['raw_frequency']
        raw_aont = request.form['raw_aont']
        raw_aofft = request.form['raw_aofft']
        raw_sleep_diary = request.form['raw_sleep_diary']
        file_formats = request.form['file_formats']
       

        if not title:
            flash('Title is required!')
        else:
            p_period = raw_duration
               
            conn = get_db_connection()
            conn.execute('UPDATE posts SET created = ? ,title = ? ,content = ? ,raw_name = ? ,raw_start_time = ? ,raw_duration = ? ,raw_uuid = ? ,raw_frequency = ? ,raw_aont = ? ,raw_aofft = ? ,raw_sleep_diary = ? ,file_formats = ? '
                       ' WHERE id = ?',
                       (created,title,content,raw_name,raw_start_time,raw_duration,raw_uuid,raw_frequency,raw_aont,raw_aofft,raw_sleep_diary,file_formats, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/kritiria', methods=('GET', 'POST'))
def kritiria(id):
    post = get_post(id)
        
    if request.method == 'POST':     
        id = request.form['id']
        title = request.form['title']
        d_File_Formats = request.form['file_formats']
        d_file = request.form['title']
        d_folder = 'data/'
        d_start_time = request.form['raw_start_time']
        d_period = request.form['raw_duration']

        if not title:
            flash('Title is required!')
        else:
            excel_id= id
            ms.Start_proc(excel_id,d_File_Formats,d_file,d_folder,d_start_time, d_period)
           # ms.Start_proc(excel_id,title,raw_start_time,raw_duration)
            ins_reg.insert_regions_from_csv('event_FLM.csv')
           # ######################   sos   16/9/23 Supmf.Make_New_File_With_Selectors(title,'event_FLM.csv')   
            
        #  main.GetActigrafy('./tmp/'+title)
        # labros 16/9/2023  
         #    raw = oa.open_file('./tmp/'+title.replace('.csv','')+'_upd.csv')
         #    raw_name=raw.name
          #   raw_start_time=str(raw.start_time)
         #    raw_duration =str(raw.duration())
         #    raw_uuid = str(raw.uuid)
         #    raw_frequency=str(raw.frequency)
         #    raw_AonT=str(raw.AonT(freq='15min', binarize=True))
         #    raw_AoffT=str(raw.AoffT(freq='15min', binarize=True))
         #    raw_sleep_diary=str(raw.sleep_diary)
         #    conn = get_db_connection()
         #    conn.execute('INSERT INTO posts (title, content,raw_name,raw_start_time,raw_duration,raw_uuid,raw_frequency,raw_AonT,raw_AoffT,raw_sleep_diary) VALUES (?,?,?,?,?,?,?,?,?,?)',
         #                (title.replace('.csv','')+'_upd.csv', 'content',raw_name,raw_start_time,raw_duration,raw_uuid,raw_frequency,raw_AonT,raw_AoffT,raw_sleep_diary))
        
         #    conn.commit()
         #    conn.close()
          # conn = get_db_connection()
          #  conn.execute('UPDATE posts SET created = ? ,title = ? ,content = ? ,raw_name = ? ,raw_start_time = ? ,raw_duration = ? ,raw_uuid = ? ,raw_frequency = ? ,raw_aont = ? ,raw_aofft = ? ,raw_sleep_diary = ? ,file_formats = ? '
          #              ' WHERE id = ?',
           #              (created,title,content,raw_name,raw_start_time,raw_duration,raw_uuid,raw_frequency,raw_aont,raw_aofft,raw_sleep_diary,file_formats, id))
          #  conn.commit()
         #   conn.close()
            return redirect(url_for('index'))

    return render_template('kritiria.html', post=post)
########################

@app.route('/<int:id>/crt_file', methods=('GET', 'POST'))
def crt_file(id):
    post = get_post(id)
   
    
    if request.method == 'POST':     
        id = request.form['id']
        title = request.form['title']
        raw_start_time = request.form['raw_start_time']
        raw_duration = request.form['raw_duration']
        file_formats = request.form['file_formats']

        if not title:
            flash('Title is required!')
        else:
            excel_id= id
          
            Supmf.Make_New_File_With_Selectors(excel_id,title,'event_FLM.csv')   
            
            raw = oa.open_file(file_formats,'./data/'+title.replace('.csv','')+'_upd.csv')
           
            raw_name=raw.name
            raw_start_time=str(raw.start_time)
            raw_duration =str(raw.duration())
            raw_uuid = str(raw.uuid)
            raw_frequency=str(raw.frequency)
            raw_AonT=str(raw.AonT(freq='15min', binarize=True))
            raw_AoffT=str(raw.AoffT(freq='15min', binarize=True))
            raw_sleep_diary=str(raw.sleep_diary)
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content,raw_name,raw_start_time,raw_duration,raw_uuid,raw_frequency,raw_AonT,raw_AoffT,raw_sleep_diary,File_Formats) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        (title.replace('.csv','')+'_upd.csv', 'content',raw_name,raw_start_time,raw_duration,raw_uuid,raw_frequency,raw_AonT,raw_AoffT,raw_sleep_diary,file_formats))
        
            conn.commit()
            conn.close()
          # conn = get_db_connection()
          #  conn.execute('UPDATE posts SET created = ? ,title = ? ,content = ? ,raw_name = ? ,raw_start_time = ? ,raw_duration = ? ,raw_uuid = ? ,raw_frequency = ? ,raw_aont = ? ,raw_aofft = ? ,raw_sleep_diary = ? ,file_formats = ? '
          #              ' WHERE id = ?',
           #              (created,title,content,raw_name,raw_start_time,raw_duration,raw_uuid,raw_frequency,raw_aont,raw_aofft,raw_sleep_diary,file_formats, id))
          #  conn.commit()
         #   conn.close()
            return redirect(url_for('index'))

    return render_template('crt_file.html', post=post)

###################################################33

@app.route('/<int:id>/plot_file', methods=('GET', 'POST'))
def plot_file(id):
    post = get_post(id)
       
    if request.method == 'POST':     
        id = request.form['id']
        title = request.form['title']
        d_File_Formats = request.form['file_formats']
        d_file = request.form['title']
        d_folder = 'data/'
        d_start_time = request.form['raw_start_time']
        d_period = request.form['raw_duration']
        if not title:
            flash('Title is required!')
        else:
                  
            main_plot.Start_proc(d_File_Formats,d_file,d_folder,d_start_time, d_period)
             
        return redirect(url_for('index'))

    return render_template('plot_file.html', post=post)

####################################################3

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

########### region

@app.route('/<int:post_id>/post_region')
def post_region(post_id):
    posts = get_regions(post_id)
   
    return render_template('regions_index.html', posts=posts)

@app.route('/<int:id>/region_edit', methods=('GET', 'POST'))
def region_edit(id):
    post = get_region_post(id)

    if request.method == 'POST':
        id = request.form['id']
        read_excel_id = request.form['read_excel_id']
        new_excel_id = request.form['new_excel_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        Sleep_Wake = request.form['Sleep_Wake']
        Interval_Status = request.form['Interval_Status']
        
        if not Sleep_Wake:
            flash('Sleep_Wake is required!')
        else:
           conn = get_db_connection()
           
           conn.execute('UPDATE regions SET read_excel_id = ? ,new_excel_id = ? ,start_date = ? ,end_date = ?  ,Sleep_Wake = ? ,Interval_Status = ? '
                        ' WHERE id = ?',
                         (read_excel_id,new_excel_id,start_date,end_date,Sleep_Wake,Interval_Status, id))
           conn.commit()
           conn.close()
           return redirect(url_for('post_region',post_id=read_excel_id))

    return render_template('regions_edit.html', post=post)

@app.route('/<int:id>/region_delete', methods=('POST',))
def region_delete(id):
    post = get_region_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM regions WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['id']))
    return redirect(url_for('post_region',post_id=post['read_excel_id']))

@app.route('/<int:id>/region_krit', methods=('GET', 'POST'))
def region_krit(id):
    post = get_post(id)
    dd = request.get_data("tm")
    
    if request.method == 'POST':     
        id = request.form['id']
        title = request.form['title']
        raw_start_time = request.form['raw_start_time']
        raw_duration = request.form['raw_duration']
        
        if not title:
            flash('Title is required!')
        else:
           
            ms.Start_proc(title,raw_start_time,raw_duration)
            Supmf. Make_New_File_With_Selectors(title,'event_FLM.csv')   
            
        #  main.GetActigrafy('./tmp/'+title)
            raw = oa.open_file('./data/'+title.replace('.csv','')+'_upd.csv')
            raw_name=raw.name
            raw_start_time=str(raw.start_time)
            raw_duration =str(raw.duration())
            raw_uuid = str(raw.uuid)
            raw_frequency=str(raw.frequency)
            raw_AonT=str(raw.AonT(freq='15min', binarize=True))
            raw_AoffT=str(raw.AoffT(freq='15min', binarize=True))
            raw_sleep_diary=str(raw.sleep_diary)
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content,raw_name,raw_start_time,raw_duration,raw_uuid,raw_frequency,raw_AonT,raw_AoffT,raw_sleep_diary) VALUES (?,?,?,?,?,?,?,?,?,?)',
                        (title.replace('.csv','')+'_upd.csv', 'content',raw_name,raw_start_time,raw_duration,raw_uuid,raw_frequency,raw_AonT,raw_AoffT,raw_sleep_diary))
        
            conn.commit()
            conn.close()
          # conn = get_db_connection()
          #  conn.execute('UPDATE posts SET created = ? ,title = ? ,content = ? ,raw_name = ? ,raw_start_time = ? ,raw_duration = ? ,raw_uuid = ? ,raw_frequency = ? ,raw_aont = ? ,raw_aofft = ? ,raw_sleep_diary = ? ,file_formats = ? '
          #              ' WHERE id = ?',
           #              (created,title,content,raw_name,raw_start_time,raw_duration,raw_uuid,raw_frequency,raw_aont,raw_aofft,raw_sleep_diary,file_formats, id))
          #  conn.commit()
         #   conn.close()
            return redirect(url_for('index'))

    return render_template('region_krit.html', post=post)

if __name__ == '__main__':  
         
      #app.run()
      app.run(debug=True  ) 
   