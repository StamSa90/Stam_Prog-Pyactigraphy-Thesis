import pyActigraphy

import os
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime
def open_file(File_Formats,file): 
    fpath = os.path.join(os.getcwd(), file)
  
    #raw = pyActigraphy.io.read_raw_awd(fpath)
    if File_Formats == "agd":
       raw = pyActigraphy.io.read_raw_agd(fpath)
    elif File_Formats == "agd":
       raw = pyActigraphy.io.read_raw_agd(fpath)
    elif File_Formats == "awd":
       raw = pyActigraphy.io.read_raw_awd(fpath)
    elif File_Formats == "bba":
       raw = pyActigraphy.io.read_raw_bba(fpath)
    elif File_Formats == "dqt":
       raw = pyActigraphy.io.read_raw_dqt(fpath)
    elif File_Formats == "mesa":
       raw = pyActigraphy.io.read_raw_mesa(fpath)
    elif File_Formats == "mtn":
       raw = pyActigraphy.io.read_raw_mtn(fpath)
    elif File_Formats == "rpx":
        raw = pyActigraphy.io.read_raw_rpx(fpath)
    elif File_Formats == "tal":
       raw = pyActigraphy.io.read_raw_tal(fpath)
    else: None
    # Η απόκρυψη των ψευδών περιόδων αδράνειας είναι ζωτικής σημασίας καθώς μπορεί να επηρεάσει ουσιαστικά τον υπολογισμό των μεταβλητών που σχετίζονται με το ρυθμό ανάπαυσης.
    raw.mask_inactivity = True
    return raw
    

def open_file_by_start_time_period(File_Formats,file,p_start_time, p_period): 
    fpath = os.path.join(os.getcwd(), file)
    #raw = pyActigraphy.io.read_raw_awd(fpath)
    if File_Formats == "agd":
       raw = pyActigraphy.io.read_raw_agd(fpath,start_time=p_start_time, period=p_period)
    elif File_Formats == "atr":
       raw = pyActigraphy.io.read_raw_atr(fpath,start_time=p_start_time, period=p_period)
    elif File_Formats == "awd":
       raw = pyActigraphy.io.read_raw_awd(fpath,start_time=p_start_time, period=p_period)
    elif File_Formats == "bba":
       raw = pyActigraphy.io.read_raw_bba(fpath,start_time=p_start_time, period=p_period)
       raw = pyActigraphy.io.read_raw_dqt(fpath,start_time=p_start_time, period=p_period)
    elif File_Formats == "mesa":
       raw = pyActigraphy.io.read_raw_mesa(fpath,start_time=p_start_time, period=p_period)
    elif File_Formats == "mtn":
       raw = pyActigraphy.io.read_raw_mtn(fpath,start_time=p_start_time, period=p_period)
    elif File_Formats == "rpx":
        print(p_period)
        print(p_start_time)
        raw = pyActigraphy.io.read_raw_rpx(fpath,start_time=p_start_time, period=p_period)
    elif File_Formats == "tal":
       raw = pyActigraphy.io.read_raw_tal(fpath,start_time=p_start_time, period=p_period)
    else: None
    # Η απόκρυψη των ψευδών περιόδων αδράνειας είναι ζωτικής σημασίας καθώς μπορεί να επηρεάσει ουσιαστικά τον υπολογισμό των μεταβλητών που σχετίζονται με το ρυθμό ανάπαυσης.
    raw.mask_inactivity = True
    return raw
    


def data_masking(raw):
    layout = go.Layout(title="Actigraphy data", xaxis=dict(title="Date time"), yaxis=dict(title="Counts/period"), showlegend=False)
    x0 =  go.Figure(data=go.Scatter(x=raw.data.index.astype(str), y=raw.data), layout=layout)
    #x0.show()

    layout1 = go.Layout(title="Data mask", xaxis=dict(title="Date time"), yaxis=dict(title="Mask"), showlegend=False)
    x1=go.Figure(data=go.Scatter(x=raw.mask.index.astype(str),y=raw.mask),layout=layout1)
    #x1.show()
    
    #raw.inactivity_length = '4h'
    x2=go.Figure(data=go.Scatter(x=raw.mask.index.astype(str),y=raw.mask),layout=layout1)
    #x2.show()

    # Kαθορίστε τις περιόδους με μη αυτόματο τρόπο
    #raw.inactivity_length = None
    #raw.add_mask_period(start='1918-01-27 09:30:00',stop='1918-01-27 17:48:00')
    x3=go.Figure(data=go.Scatter(x=raw.mask.index.astype(str),y=raw.mask),layout=layout1)
    #x3.show()

   # add_mask_periodsλειτουργία επιτρέπει στους χρήστες να χρησιμοποιούν ένα αρχείο για να καθορίσουν πολλές επιπλέον περιόδους μάσκας ταυτόχρονα.
    # raw.add_mask_periods(os.path.join(os.getcwd(), 'tmp/example_masklog.csv'))
    x4=go.Figure(data=go.Scatter(x=raw.mask.index.astype(str),y=raw.mask),layout=layout1)
    #x4.show()

    x5=go.Figure(data=[go.Scatter(x=raw.data.index, y=raw.data)], layout=layout1)
    #x5.show() 
    sadeh = raw.Sadeh()
    scripps = raw.Scripps()
    CK = raw.CK()
    ###############################33


    fig = make_subplots(rows=2, cols=3)

    fig.add_trace(
      go.Scatter(x=raw.data.index.astype(str), y=raw.data, name='Data'),
      row=1, col=1
   )

    fig.add_trace(
      go.Scatter(x=raw.mask.index.astype(str),y=raw.mask, name='mask'),
      row=1, col=2
   )
    fig.add_trace(
      go.Scatter(x=sadeh.index.astype(str),y=sadeh, yaxis='y2', name='Sadeh') ,
      row=1, col=3
   )
    fig.add_trace(
      go.Scatter(x=scripps.index.astype(str),y=scripps, yaxis='y2', name='scripps') ,
      row=2, col=1
   )
    fig.add_trace(
      go.Scatter(x=CK.index.astype(str),y=CK, yaxis='y2', name='CK') ,
      row=2, col=2
  )

    
    fig.update_layout(height=600, width=2000, title_text="Side By Side Subplots")
    fig.show()
    #################################


   #raw_name = raw.name
   # raw_start_time =  str(raw.start_time)
   # raw_duration = str(raw.duration())
   # raw_uuid = str(raw.uuid)
   # raw_frequency = str(raw.frequency)
   # raw_AonT = str(raw.AonT(freq='15min', binarize=True))
   # raw_AoffT = str(raw.AoffT(freq='15min', binarize=True))

   # return raw_name
    #Όνομα θέματος:
  #  print('Όνομα θέματος: '+raw.name)
    #Ώρα έναρξης της απόκτησης δεδομένων
    #print('Ώρα έναρξης της απόκτησης δεδομένων: '+str(raw.start_time))
    #Διάρκεια απόκτησης δεδομένων:
   # print('Διάρκεια απόκτησης δεδομένων:'+str(raw.duration()))
    #Αριθμός σειράς της συσκευής:
   # print('Αριθμός σειράς της συσκευής :'+str(raw.uuid))
    #Συχνότητα απόκτησης:
   # print('Συχνότητα απόκτησης: '+str(raw.frequency))

    #Χρόνοι έναρξης
   # print('Χρόνοι έναρξης'+str(raw.AonT(freq='15min', binarize=True)))
    #Mετατόπισης δραστηριότητας
   # print('Mετατόπισης δραστηριότητας '+raw.AoffT(freq='15min', binarize=True))
    #How to plot the data¶
    #First, create a layout for the plot:

    
