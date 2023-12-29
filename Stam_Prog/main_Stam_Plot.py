
import pyActigraphy
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pyActigraphy.analysis import Fractal
import numpy as np
from matplotlib.widgets import RectangleSelector
import numpy as np
import Py_actigrafi_app as Py
import matplotlib.pyplot as plt
x11 =None
x21 =None
def  pyActigraphy_analysis_import_FLM(d_File_Formats,d_file,d_folder,d_start_time, d_period):
    # raw0 = pyActigraphy.io.read_raw_rpx(fpath, start_time=p_start_time, period=p_period)
    raw0 = Py.open_file_by_start_time_period(d_File_Formats,d_file,d_folder,d_start_time, d_period)
    layout = go.Layout(title="Actigraphy data", xaxis=dict(title="Date time"), yaxis=dict(title="Counts/period"), showlegend=False)
    layout.update(yaxis2=dict(title='Classification',overlaying='y',side='right'), showlegend=True);
    sadeh = raw0.Sadeh()
    scripps = raw0.Scripps()
    CK = raw0.CK()

    
    x0 = go.Figure(data=[go.Scatter(x=raw0.data.index, y=raw0.data),
     go.Scatter(x=sadeh.index.astype(str),y=sadeh, yaxis='y2', name='Sadeh'),
     go.Scatter(x=scripps.index.astype(str),y=scripps, yaxis='y2', name='Scripps'),
     go.Scatter(x=CK.index.astype(str),y=CK, yaxis='y2', name='CK')], layout=layout)

    x0.show()
    return raw0

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

def Start_proc(d_File_Formats,d_file,d_folder,d_start_time, d_period):
    #fpath = os.path.join(os.getcwd(), "./data/"+csv_file)
    raw0 = pyActigraphy_analysis_import_FLM(d_File_Formats,d_file,d_folder,d_start_time, d_period)
    fig = yActigraphy_analysis_import_Fractal(raw0)
    fig2 = multi_FRACTAL_DFA(raw0)
    np_proc(fig2,raw0)
    Make_A_New_plotting_range(raw0,fig)


#fpath = os.path.join(os.getcwd(), 'example.csv')
#p_start_time= '2022-07-18 13:00:00'
#p_period = '1 day'
#raw0 = pyActigraphy_analysis_import_FLM(fpath,p_start_time, p_period)
#fig = yActigraphy_analysis_import_Fractal(raw0)
#fig2 = multi_FRACTAL_DFA(raw0)
#np_proc(fig2)
#Make_A_New_plotting_range(raw0,fig)


