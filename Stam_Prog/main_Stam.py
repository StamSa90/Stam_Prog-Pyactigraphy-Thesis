import csv
import pyActigraphy
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pyActigraphy.analysis import Fractal
import numpy as np
from matplotlib.widgets import RectangleSelector
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import matplotlib.dates as mdates
from datetime import datetime
import Py_actigrafi_app  as Py_op


def  pyActigraphy_analysis_import_FLM(d_excel_id,d_File_Formats,d_file,d_folder,d_start_time, d_period):
     
    excel_id =d_excel_id
    raw0 = Py_op.open_file_by_start_time_period(d_File_Formats,d_file,d_folder,d_start_time, d_period)
   
    layout = go.Layout(title="Actigraphy data", xaxis=dict(title="Date time"), yaxis=dict(title="Counts/period"), showlegend=False)
    layout.update(yaxis2=dict(title='Classification',overlaying='y',side='right'), showlegend=True);
    #sadeh = raw0.Sadeh()
    #scripps = raw0.Scripps()
    #CK = raw0.CK()
    dt_rows =[]
    with open('./data/event_FLM.csv', 'w',newline='') as f_object:
        List = ["excel_id","Start_Date","End_Date","Sleep_Wake","Interval_Status"]   
        writer_object = csv.writer(f_object, quoting=csv.QUOTE_ALL)

        writer_object.writerow(List)

        # Close the file object
        f_object.close()

    #x0 = go.Figure(data=[go.Scatter(x=raw0.data.index, y=raw0.data)  ], layout=layout )
        #,go.Scatter(x=sadeh.index.astype(str),y=sadeh, yaxis='y2', name='Sadeh')
        #,go.Scatter(x=scripps.index.astype(str),y=scripps, yaxis='y2', name='Scripps')
        ##  ,go.Scatter(x=CK.index.astype(str),y=CK, yaxis='y2', name='CK')
    x = raw0.data.index  
    y = raw0.data 

    fig, x0 = plt.subplots(figsize=(8, 6))
    

    x0.plot(x, y)
    x0.xaxis.set_major_locator(mdates.HourLocator(12))
    x0.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%b-%d"))
    x0.set_title("Actigraphy data")
    x0.xaxis.set_minor_locator(mdates.HourLocator(np.arange(0,24,2)))
    x0.xaxis.set_minor_formatter(mdates.DateFormatter("%H"))
    x0.set_ylabel = "Counts/period"
    x0.set_xlabel = "Date time"
    x0.legend =False
    x0.tick_params(which="major", axis="x", pad=14, size=2)
    x0.tick_params(which="minor", axis="x", labelsize=8)  

    span = SpanSelector(
            x0,
            onselect,
            "horizontal",
            useblit=True,
            props=dict(alpha=0.5, facecolor="tab:blue"),
            interactive=True,
            drag_from_anywhere=True)
  
    plt.show()
    # Set useblit=True on most backends for enhanced performance.
    

    return raw0

def onselect(xmin, xmax):
#indmin, indmax = np.searchsorted(x, (xmin, xmax))
#    
    
    
    start_date = str(mdates.num2date(xmin))[:19]   
    end_date   = str(mdates.num2date(xmax))[:19] 
    Sleep_Wake= ""
    Interval_Status = ""
    # Import writer class from csv module

    # List that we want to add as a new row
    List = [excel_id,start_date, end_date ,Sleep_Wake,Interval_Status]

    # Open our existing CSV file in append mode
    # Create a file object for this file
    with open('./data/event_FLM.csv', 'a',newline='') as f_object:

        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = csv.writer(f_object, quoting=csv.QUOTE_ALL)

        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(List)

        # Close the file object
        f_object.close()

def yActigraphy_analysis_import_Fractal(raw0):
    profile = Fractal.profile(raw0.data.values)
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(go.Scatter(x=raw0.data.index.astype(str),y=raw0.data.values, name='Data'),
        secondary_y=False,)

    fig.add_trace(go.Scatter(x=raw0.data.index.astype(str),y=profile, name='Profile'),
        secondary_y=True,)

    # Add figure title
    fig.update_layout(
        title_text="Detrended and integrated data profile"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date time")
    # Set y-axes titles
    fig.update_yaxes(title_text="Activity counts", secondary_y=False)
    #fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

    fig.show()    
    return fig

def  multi_FRACTAL_DFA(raw0):
    n_array = np.geomspace(10, 1440, num=50, endpoint=True, dtype=int) # Numbers spaced evenly on a log scale, ranging from an ultradian time scale (10 min.) to a circadian one (1440 min, i.e. 24h)
    q_array = [1,2,3,4,5,6]
    MF_F_n = Fractal.mfdfa(raw0.data,n_array,q_array,deg=1)
    fig2 = go.Figure(data=[
    go.Scatter(x=n_array,y=np.log(MF_F_n[:,q]), name='Data fluctuation (q-th order: {})'.format(q_array[q]),mode='markers+lines') for q in range(len(q_array))])
    fig2.update_layout(
    height=800, width=800,
    xaxis=dict(title='Time (min.)',type='log'),
    yaxis=dict(title='log(F(n))'))
    fig2.show()
    return fig2

def np_proc(fig2,raw0):
    n_array = np.geomspace(10, 1440, num=50, endpoint=True, dtype=int) # Numbers spaced evenly on a log scale, ranging from an ultradian time scale (10 min.) to a circadian one (1440 min, i.e. 24h)
    q_array = [1,2,3,4,5,6]
    MF_F_n = Fractal.mfdfa(raw0.data,n_array,q_array,deg=1)
    fig2 = go.Figure(data=[
        go.Scatter(x=n_array,y=np.log(MF_F_n[:,q]), name='Data fluctuation (q-th order: {})'.format(q_array[q]),mode='markers+lines') for q in range(len(q_array))])
    fig2.update_layout(
        height=800, width=800,
        xaxis=dict(title='Time (min.)',type='log'),
        yaxis=dict(title='log(F(n))'))
    fig2.show()

def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    
    print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
    print(" The button you used were: %s %s" % (eclick.button, erelease.button))

def line_select_callback1(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
    print(" The button you used were: %s %s" % (eclick.button, erelease.button))
    return x1,x2,y1,y2

def toggle_selector(event):
    print(' Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)

def Make_A_New_plotting_range(raw0,fig):   
   fig, current_ax = plt.subplots()                 # make a new plotting range
   N = 10000                                    # If N is large one can see
   x = np.linspace(0.0, 10.0, N)                    # improvement by use blitting!
   plt.plot(raw0.data)
   print("\n      click  -->  release")
   toggle_selector.RS = RectangleSelector(current_ax, line_select_callback,
                                      drawtype='box', useblit=True,
                                     button=[1, 3],  # don't use middle button
                                     minspanx=5, minspany=5,
                                      spancoords='pixels',
                                     interactive=True)
   plt.show()

def Start_proc(d_excel_id,d_File_Formats,d_file,d_folder,d_start_time, d_period):
    global excel_id
    excel_id = d_excel_id
        
    raw0 = pyActigraphy_analysis_import_FLM(d_excel_id,d_File_Formats,d_file,d_folder,d_start_time, d_period)
  #  fig = yActigraphy_analysis_import_Fractal(raw0)
  #  fig2 = multi_FRACTAL_DFA(raw0)
  #  np_proc(fig2,raw0)
  #  Make_A_New_plotting_range(raw0,fig)





