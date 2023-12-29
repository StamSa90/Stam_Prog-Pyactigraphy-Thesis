import pyActigraphy
import plotly.graph_objects as go
import os
import fld
import numpy as np
from pyActigraphy.analysis import SSA
from pyActigraphy.analysis import FLM 
from pyActigraphy.analysis import Cosinor 
from plotly.subplots import make_subplots
from pyActigraphy.analysis import Fractal

def open_file(File_Formats,p_folder,p_file): 
    # fpath = os.path.join(os.getcwd(), file)
    #raw = pyActigraphy.io.read_raw_awd(fpath)
    fpath_folder = os.path.join(os.path.dirname(fld.__file__),p_folder)
    fpath = fpath_folder + p_file
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
    elif File_Formats == "batch":
       raw = pyActigraphy.io.read_raw(fpath)
       
    else: None
    # Η απόκρυψη των ψευδών περιόδων αδράνειας είναι ζωτικής σημασίας καθώς μπορεί να επηρεάσει ουσιαστικά τον υπολογισμό των μεταβλητών που σχετίζονται με το ρυθμό ανάπαυσης.
   # raw.mask_inactivity = True
    return raw

def open_file_by_start_time_period(p_File_Formats,p_file,p_folder,p_start_time, p_period): 
   
    p_fpath = os.path.join(os.path.dirname(fld.__file__),p_folder)
    fpath = p_fpath + p_file
    if p_File_Formats == "agd":
       raw = pyActigraphy.io.read_raw_agd(fpath,start_time=p_start_time, period=p_period)
    elif p_File_Formats == "atr":
       raw = pyActigraphy.io.read_raw_atr(fpath,start_time=p_start_time, period=p_period)
    elif p_File_Formats == "awd":
       raw = pyActigraphy.io.read_raw_awd(fpath,start_time=p_start_time, period=p_period)
    elif p_File_Formats == "bba":
       raw = pyActigraphy.io.read_raw_bba(fpath,start_time=p_start_time, period=p_period)
       raw = pyActigraphy.io.read_raw_dqt(fpath,start_time=p_start_time, period=p_period)
    elif p_File_Formats == "mesa":
       raw = pyActigraphy.io.read_raw_mesa(fpath,start_time=p_start_time, period=p_period)
    elif p_File_Formats == "mtn":
       raw = pyActigraphy.io.read_raw_mtn(fpath,start_time=p_start_time, period=p_period)
    elif p_File_Formats == "rpx":
        print(p_period)
        print(p_start_time)
        raw = pyActigraphy.io.read_raw_rpx(fpath,start_time=p_start_time, period=p_period)
    elif p_File_Formats == "tal":
       raw = pyActigraphy.io.read_raw_tal(fpath,start_time=p_start_time, period=p_period)
    else: None
    # Η απόκρυψη των ψευδών περιόδων αδράνειας είναι ζωτικής σημασίας καθώς μπορεί να επηρεάσει ουσιαστικά τον υπολογισμό των μεταβλητών που σχετίζονται με το ρυθμό ανάπαυσης.
    #raw.mask_inactivity = True
    return raw
    
def General(p_File_Formats,p_folder,p_file): 

      raw =open_file(p_File_Formats,p_folder,p_file)
      name = raw.name
      start_time = raw.start_time
      duration = raw.duration()
      uuid = raw.uuid
      frequency = raw.frequency
      AonT  = raw.AonT(freq='15min', binarize=True)
      AoffT = raw.AoffT(freq='15min', binarize=True)


      #### BATCH ####
      if p_File_Formats == "batch":
         
         # Check how many files have been read(batch)

         batch_len = len(raw.readers)
         batch_names = raw.names()

         # Check the duration of the recording
         batch_duration = raw.duration()

         #Most rest-activity rhythm related variables are available:
         batch_IS =  raw.IS()
         batch_kAR = raw.kAR(0)
         # Manual analysis
         for iread in raw.readers:
            print("Object type: {}. Name: {}. Duration of the recording: {}. Number of acquisition points: {}".format(type(iread),iread.name,iread.duration(),len(iread.data)))

      #How to plot the data

def Data(p_File_Formats,p_folder,p_file):
   raw =open_file(p_File_Formats,p_folder,p_file)
   layout = go.Layout(
         title="Actigraphy data",
         xaxis=dict(title="Date time"),
         yaxis=dict(title="Counts/period"),
         showlegend=False )
   plot_data = go.Figure(data=[go.Scatter(x=raw.data.index.astype(str), y=raw.data)], layout=layout)

   plot_data.show()

def Daily_activity_profile(p_File_Formats,p_folder,p_file):
   raw =open_file(p_File_Formats,p_folder,p_file)
# Daily activity profile
   layout = go.Layout(
               title="Actigraphy data",
               xaxis=dict(title="Date time"),
               yaxis=dict(title="Counts/period"),
               showlegend=False
            )
   layout.update(title="Daily activity profile",xaxis=dict(title="Date time"), showlegend=False);

      # With pyActigraphy, you can easily control the resampling frequency (i.e. the resolution at which you want to inspect the data). It is also possible to binarize the data: 0 for inactive or 1 for active.

      #help(raw.average_daily_activity)

   daily_profile = raw.average_daily_activity(freq='15min', cyclic=False, binarize=False)

   plot_daily_profile = go.Figure(data=[go.Scatter(x=daily_profile.index.astype(str), y=daily_profile)], layout=layout)

   plot_daily_profile.show()

# https://ghammad.github.io/pyActigraphy/pyActigraphy-Masking.html
def Data_Masking(p_File_Formats,p_folder,p_file):
      raw =open_file(p_File_Formats,p_folder,p_file)
      #  Plot the data 
      # τα ακυρωσα εγω
    # layout = go.Layout(title="Actigraphy data", xaxis=dict(title="Date time"), yaxis=dict(title="Counts/period"), showlegend=False)
    #  Plot_Data = go.Figure(data=go.Scatter(x=raw.data.index.astype(str), y=raw.data), layout=layout)
    #  Plot_Data.show()
      
      # Mask inactive data
      # Create a mask automatically
      # raw.frequency    Timedelta('0 days 00:01:00')

      # The duration corresponds either to the minimal number of inactive epochs (ex: duration=120)
      # or the minimal length of the inactive period (duration='2h00min')
      raw.create_inactivity_mask(duration='2h00min')
      # inactivity_length =raw.inactivity_length   # 120
      #  WARNING: Creating a mask does not mean it is applied. Cf. next section.**
      layout = go.Layout(title="Data mask", xaxis=dict(title="Date time"), yaxis=dict(title="Mask"), showlegend=False)
      Data_mask =go.Figure(data=go.Scatter(x=raw.mask.index.astype(str),y=raw.mask),layout=layout)
      # Periods in the data for which the mask is equal to zero will be masked (once the mask is applied)
      Data_mask.show()

      raw.inactivity_length = '4h'
      Data_mask_inactivity_length = go.Figure(data=go.Scatter(x=raw.mask.index.astype(str),y=raw.mask),layout=layout)
      Data_mask_inactivity_length.show()
     
     #  Create a mask specify the periods manually
def Data_Masking_manually(p_File_Formats,p_folder,p_file,M_start,M_stop):
    raw =open_file(p_File_Formats,p_folder,p_file)
    raw.inactivity_length = None       
    # raw.mask      message=  Could not create a mask

    #  add_mask_period
    raw.add_mask_period(start=M_start,stop=M_stop)
    layout = go.Layout(title="Data mask", xaxis=dict(title="Date time"), yaxis=dict(title="Mask"), showlegend=False)
    add_mask_period = go.Figure(data=go.Scatter(x=raw.mask.index.astype(str),y=raw.mask),layout=layout)
    add_mask_period.show()

    # add_mask_periods   
def Data_Masking_add_masklog_periods(p_File_Formats,p_folder,p_file):
    raw =open_file(p_File_Formats,p_folder,p_file)
    # Reset mask
    #raw.inactivity_length = None
    # raw.add_mask_periods(os.path.join(os.path.dirname(pyActigraphy.__file__),'tests/data/example_masklog.csv'))
    print(os.path.join(os.path.dirname(fld.__file__)))
    raw.add_mask_periods(os.path.join(os.path.dirname(fld.__file__),'data/example_masklog.csv'))
    layout = go.Layout(title="Data_Masking_add_mask_periods", xaxis=dict(title="Date time"), yaxis=dict(title="Mask"), showlegend=False)
    Data_Masking_add_mask_periods = go.Figure(data=go.Scatter(x=raw.mask.index.astype(str),y=raw.mask),layout=layout)
    
    Data_Masking_add_mask_periods.show()
    # Apply the mask
    # raw.IS()   
    # 0.44565929945478583
    # raw.mask_inactivity = True
    # raw.IS()
    # 0.5097482433325218
    # raw.mask_inactivity = False
    # raw.IS()
    # 0.44565929945478583

#https://ghammad.github.io/pyActigraphy/pyActigraphy-SSt-log.html    
# Cleaning files individually
def Cleaning_files_individually(d_File_Formats,d_folder,d_file,d_start_time,d_period):
     
    raw = open_file_by_start_time_period(d_File_Formats,d_file,d_folder,d_start_time, d_period)
    before_discard_invalid_sequences   = go.Figure(data=[go.Scatter(x=raw.data.index, y=raw.data)], layout=go.Layout())
    before_discard_invalid_sequences.show()
    # Check the start time of the actigraphy recording
    # raw.start_time  Timestamp('1918-01-23 13:58:00')
    # Check the duration of the recording
    # raw.start_time  Timestamp('1918-01-23 13:58:00')
    # Check the duration of the recording
    # raw.duration()   Timedelta('12 days 18:41:00')


    # How Cleaning files individually
    #fpath = os.path.join(os.path.dirname(fld.__file__),d_folder)
    #raw_cropped = pyActigraphy.io.read_raw_awd(fpath+d_file, start_time=d_start_time, period=d_period)
    raw_cropped = open_file_by_start_time_period(d_File_Formats,d_file,d_folder,d_start_time, d_period)
    # raw_cropped.start_time   Timestamp('1918-01-24 08:00:00')
    # raw_cropped.duration()   Timedelta('9 days 00:01:00')

    raw = open_file(d_File_Formats,d_folder,d_file) 
    #pyActigraphy.io.read_raw_awd(fpath+d_file)
    
    Cleaning_files_individually = go.Figure(data=[go.Scatter(x=raw_cropped.data.index, y=raw_cropped.data)], layout=go.Layout())
    Cleaning_files_individually.show()
    # raw.IS() 0.527656245354158
    # raw_cropped.IS()  0.8290854646594275

def Read_a_sleep_diary(d_File_Formats,d_folder,d_file,d_sleep_diary_file,d_Add_custom_states_file):
    fpath = os.path.join(os.path.dirname(fld.__file__),d_folder)
    #raw = pyActigraphy.io.read_raw_awd(fpath+d_file)
    raw =open_file(d_File_Formats,d_folder,d_file)
    # Check the start time of the actigraphy recording    raw.start_time Timestamp('1918-01-23 13:58:00')
    #  
    # Check the duration of the recording    raw.duration() Timedelta('12 days 18:41:00')
    sleep_diary = raw.read_sleep_diary(fpath + d_sleep_diary_file)
    # raw.sleep_diary.name  'EXAMPLE_01'
    # raw.sleep_diary.diary  To access to the data contained in the sleep diary:
    # raw.sleep_diary.summary()  A summary function is available. It returns the count/mean/std/min/25%/50%/75%/max of the durations found for each state in the sleep diary
    # raw.sleep_diary.state_infos('NIGHT')  (Timedelta('0 days 07:50:30'), Timedelta('0 days 00:59:19.353873949'))
    # raw.sleep_diary.total_nap_time()  (Timedelta('0 days 00:50:30'), Timedelta('0 days 00:15:10.494371207'))
    # raw.sleep_diary.total_nowear_time()  (Timedelta('0 days 00:41:30'), Timedelta('0 days 00:16:15.807358037'))
   
    # Plot the data with sleep diary
    # raw.sleep_diary.shaded_area {'type': 'rect', 'xref': 'x', 'yref': 'paper', 'x0': 0, 'y0': 0,  'x1': 1, 'y1': 1, 'fillcolor': '', 'opacity': 0.5, 'layer': 'below', 'line': {'width': 0}}
    layout = go.Layout(title="Actigraphy data",xaxis=dict(title="Date time"),yaxis=dict(title="Counts/period"),shapes=raw.sleep_diary.shapes(),showlegend=False)
    sleep_diary = go.Figure(data=go.Scatter(x=raw.data.index, y=raw.data), layout=layout)
    sleep_diary.show()

   # Global modifications
    raw.sleep_diary.shaded_area['opacity'] = 1
    layout.update(shapes=raw.sleep_diary.shapes());
    
    Global_modifications = go.Figure(data=go.Scatter(x=raw.data.index, y=raw.data), layout=layout)
    Global_modifications.show()

    # # Access to colours for each state
    #  raw.sleep_diary.state_colour  {'NAP': '#7bc043', 'NIGHT': '#d3d3d3', 'NOWEAR': '#ee4035'}
    
   # One state modification
    raw.sleep_diary.state_colour['NIGHT'] = 'rgb(140,95,148)'

   # # Check colour modification
   # raw.sleep_diary.state_colour  {'NAP': '#7bc043', 'NIGHT': 'rgb(140,95,148)', 'NOWEAR': '#ee4035'}
    layout.update(shapes=raw.sleep_diary.shapes());
    Check_colour_modification = go.Figure(data=go.Scatter(x=raw.data.index, y=raw.data), layout=layout)
    Check_colour_modification.show()

   # Local modifications of the first shape
    shapes = raw.sleep_diary.shapes()
    shapes[0]['fillcolor'] = 'rgb(0,255,200)'
    layout.update(shapes=shapes);
    Local_modifications_of_the_first_shape = go.Figure(data=go.Scatter(x=raw.data.index, y=raw.data), layout=layout)
    Local_modifications_of_the_first_shape.show()
   
   # Add custom states
   # # Default implemented states
   # raw.sleep_diary.state_index   {'ACTIVE': 2, 'NAP': 1, 'NIGHT': 0, 'NOWEAR': -1}
   # To add a custom state, all indices and their colours have to be specified during the reading of the sleep diary:
    raw.read_sleep_diary( fpath + d_Add_custom_states_file ,state_index=dict(ACTIVE=2, NAP=1, NIGHT=0, NOWEAR=-1, AWAKE_IN_BED=3),
    state_colour=dict(NAP='#7bc043',NIGHT='#d3d3d3',NOWEAR='#ee4035', AWAKE_IN_BED='rgb(143, 19, 131)'  ))
    layout = go.Layout(title="Actigraphy data",xaxis=dict(title="Date time"),yaxis=dict(title="Counts/period"),shapes=raw.sleep_diary.shapes(),showlegend=False)
    Add_custom_states = go.Figure(data=go.Scatter(x=raw.data.index, y=raw.data), layout=layout)
    Add_custom_states.show()
    # raw.sleep_diary.state_infos('AWAKE_IN_BED')   (Timedelta('0 days 01:30:00'), NaT)

# https://ghammad.github.io/pyActigraphy/pyActigraphy-Sleep-Algorithms.html
#***********************Automatic detection of rest/activity periods with pyActigraphy
def Automatic_detection_of_rest_activity_periods(d_folder,d_file,d_start_time,d_period,d_language):
   fpath = os.path.join(os.path.dirname(fld.__file__),d_folder)
   raw = pyActigraphy.io.read_raw_rpx(fpath+d_file, start_time=d_start_time, period=d_period, language=d_language)
   
   # Epoch-by-epoch rest/activity scoring algorithms
   layout = go.Layout(title="Rest/Activity detection",xaxis=dict(title="Date time"), yaxis=dict(title="Counts/period"), showlegend=False)
   
   # Cole-Kripke  help(raw.CK)
   CK = raw.CK()
   layout.update(yaxis2=dict(title='Classification',overlaying='y',side='right'), showlegend=True);
   Cole_Kripke = go.Figure(data=[ go.Scatter(x=raw.data.index.astype(str),y=raw.data, name='Data'), 
                                  go.Scatter(x=CK.index.astype(str),y=CK, yaxis='y2', name='CK')], layout=layout)
   Cole_Kripke.show()

   # Sadeh’s and Scripps’ algorithms
   sadeh = raw.Sadeh()
   scripps = raw.Scripps()
   Sadehs_Scripps = go.Figure(data=[go.Scatter(x=raw.data.index.astype(str),y=raw.data, name='Data'),
                                         go.Scatter(x=sadeh.index.astype(str),y=sadeh, yaxis='y2', name='Sadeh'),
                                         go.Scatter(x=scripps.index.astype(str),y=scripps, yaxis='y2', name='Scripps')], layout=layout)
   Sadehs_Scripps.show()
  
  # Oakley’s algorithm  help(raw.Oakley)
   oakley = raw.Oakley(threshold=40)
  #  Automatic threshold 
   oakley_auto = raw.Oakley(threshold='automatic')
  
   Oakleys_algorithm = go.Figure(data=[ go.Scatter(x=raw.data.index.astype(str),y=raw.data, name='Data'),
                                        go.Scatter(x=oakley.index.astype(str),y=sadeh, yaxis='y2', name='Oakley (thr: medium)'),
                                        go.Scatter(x=oakley_auto.index.astype(str),y=scripps, yaxis='y2', name='Oakley (thr: automatic)')], layout=layout)
   Oakleys_algorithm.show()

# Consolidated activity/rest period detection
   # Crespo’s algorithm    help(raw.Crespo)
   # This is a threshold-based algorithm that used morphological filters to “clean” short periods of activity (rest) surrounded by periods of rest (acitivity).
 
def  Consolidated_activity_rest_period_detection(p_File_Formats,p_folder,p_file): 
###   only awd
         raw =open_file(p_File_Formats,p_folder,p_file)
         crespo = raw.Crespo()
         crespo_6h = raw.Crespo(alpha='6h')
         crespo_zeta = raw.Crespo(estimate_zeta=True)
         layout = go.Layout(title="Rest/Activity detection",xaxis=dict(title="Date time"), yaxis=dict(title="Counts/period"), showlegend=False)
         Plot_crespo = go.Figure(data=[go.Scatter(x=raw.data.index.astype(str),y=raw.data, name='Data'),
                         go.Scatter(x=crespo.index.astype(str),y=crespo, yaxis='y2', name='Crespo'),
                         go.Scatter(x=crespo_6h.index.astype(str),y=crespo_6h, yaxis='y2', name='Crespo (6h)'),
                         go.Scatter(x=crespo_zeta.index.astype(str),y=crespo_zeta, yaxis='y2', name='Crespo (Automatic)')], layout=layout)
         Plot_crespo.show()
         
         aot = raw.Crespo_AoT()     
         # aot[0]-aot[1]

def Roennebergs_algorithm (p_File_Formats,p_folder,p_file):
      raw =open_file(p_File_Formats,p_folder,p_file)
         #   help(raw.Roenneberg)
      roenneberg = raw.Roenneberg()
      roenneberg_thr = raw.Roenneberg(threshold=0.25, min_seed_period='15min')
      layout = go.Layout(title="Rest/Activity detection",xaxis=dict(title="Date time"), yaxis=dict(title="Counts/period"), showlegend=False)
      layout.update(yaxis2=dict(title='Classification',overlaying='y',side='right'), showlegend=True);
      Plot_Roennebergs = go.Figure(data=[ go.Scatter(x=raw.data.index.astype(str),y=raw.data, name='Data'),
                       go.Scatter(x=roenneberg.index.astype(str),y=roenneberg, yaxis='y2', name='Roenneberg'),
                       go.Scatter(x=roenneberg_thr.index.astype(str),y=roenneberg_thr, yaxis='y2', name='Roenneberg (Thr:0.25)')], layout=layout)
      Plot_Roennebergs.show()

   # https://ghammad.github.io/pyActigraphy/pyActigraphy-Cosinor.html
#  Cosinor analysis
def Cosinor_analysis(d_File_Formats,d_folder,d_file,d_start_time,d_period):
  
    
    raw = open_file_by_start_time_period(d_File_Formats,d_file,d_folder,d_start_time, d_period)
    cosinor = Cosinor()
    # Initial fit values  cosinor.fit_initial_params.pretty_print()
    cosinor.fit_initial_params['Period'].value = 2880
    
    #B y default, the initial values of the cosine fit functions are the following:
    # cosinor.fit_initial_params.pretty_print() 
    # By default, none of the fit parameters are fixed and will be estimated from the data. However, in some cases, 
    # it might be convenient to fix the initial of a parameter and not let it vary during the fit procedure.
    # cosinor.fit_initial_params['Period'].value = 1440
    # cosinor.fit_initial_params['Period'].vary = False

    # Analysis of a single subject
    fig = go.Figure(go.Scatter(x=raw.data.index.astype(str),y=raw.data))
    fig.show()

    # results = cosinor.fit(raw.data, verbose=True) # Set verbose to True to print the fit output
    # To access the best fit parameter values:
    # results.params['Mesor'].value

    # It is also possible to transform them to a dictionary:
    # results.params.valuesdict()

    # The results object contains also informations about the goodness-of-fit:
    # results.aic # Akaike information criterium
    # results.redchi # Reduced Chi^2
    # help(cosinor.best_fit)


    results = cosinor.fit(raw.data, verbose=True) # Set verbose to True to print the fit output
    best_fit = cosinor.best_fit(raw.data, results.params)
    fig = go.Figure(  data=[
         go.Scatter(x=raw.data.index.astype(str),y=raw.data,name='Raw data'),
         go.Scatter(x=best_fit.index.astype(str),y=best_fit,name='Best fit') ] )

    fig.show()

# https://ghammad.github.io/pyActigraphy/pyActigraphy-FLM.html
# Functional linear modelling
def Functional_linear_modelling(d_File_Formats,d_folder,d_file,d_start_time,d_period):
   
   # create objects for layout and traces
   layout = go.Layout(autosize=False, width=850, height=600, title="",xaxis=dict(title=""), shapes=[], showlegend=True)
   # Define the path to your input data
   raw = open_file_by_start_time_period(d_File_Formats,d_file,d_folder,d_start_time, d_period)
   # Basis function expansion
   # Using a Fourier basis expansion
   # Resampling frequency for the daily activity profile
   freq='1min'
   # The number of basis functions is max_order*2+1 (1 constant + n cosine functions + n sine functions)
   max_order = 9
   #First, let’s define a FLM object with “Fourier” functions as a basis:
   flm = FLM(basis='fourier',sampling_freq=freq,max_order=max_order)
   # To estimate the scalar coefficients of the basis expansion (“beta” coefficients), use the fit function:
   # By setting the "verbose" parameter to True, the result of least-square fit is displayed:
   flm.fit(raw,verbose=True)
   # Now, to reconstruct the signal using its expansion up to the 9th order:
   flm_est = flm.evaluate(raw)
   # And compare it to the original daily profile:
   daily_avg = raw.average_daily_activity(binarize=False,freq=freq)

   # set x-axis labels and their corresponding data values
   labels = ['00:00', '06:00', '12:00', '18:00']
   tickvals = ['00:00:00', '06:00:00', '12:00:00', '18:00:00']

   layout = go.Layout(
      autosize=False, width=900, height=600,
      title="Daily profile",
      xaxis=dict(
         title="Time of day (HH:MM)",
         ticktext=labels,
         tickvals=tickvals),
      yaxis=dict(title="Counts (a.u)"),
      shapes=[], showlegend=True)

   Plot_flm= go.Figure(data=[go.Scatter(x=daily_avg.index.astype(str),y=daily_avg,name='Raw activity'),
                   go.Scatter(x=daily_avg.index.astype(str),y=flm_est,name='Fourier expansion (9th order)')],layout=layout)
   Plot_flm.show()

   # Using B_splines

   # B-splines are piecewise polynomial curves. By definition, they ensure the aforementioned “smoothness” of the data representation.
   daily_avg = raw.average_daily_activity(binarize=False,freq="30min")

   # in order to check how the data are interpolated, let’s set the resampling frequency at 30 min.
   flm_spline = FLM(basis='spline',sampling_freq='30min',max_order=3)

   # Again, like for the Fourier basis, the evaluation of the B-spline representation is performed via the fit function:
   flm_spline.fit(raw, verbose=False)

   # Now, let’s evaluate the splines:
   # The "r" parameter represents the ratio between the number of points at which the spline is evaluated and the original number of points.
   r = 10
   spline_est = flm_spline.evaluate(raw,r=r)
   # To visualize the result, one needs to create 2 different X axis as there are “r” times more points in the evaluated spline:
   t = np.linspace(0,daily_avg.index.size,daily_avg.index.size,endpoint=True)
   t_10 = np.linspace(0,daily_avg.index.size,daily_avg.index.size*r,endpoint=True)

   data = [go.Scatter(x=t,y=daily_avg,name='Raw activity'),
           go.Scatter(x=t_10,y=spline_est,name='B-spline')  ]
   
   Plot_B_splines = go.Figure(data=data, layout=layout)
   Plot_B_splines.show()

   #  Gaussian kernel smoothing
   # help(FLM.smooth)

   daily_avg = raw.average_daily_activity(freq=flm.sampling_freq, binarize=False)
   names = ['Raw activity', 'Scott', 'Silverman', 'Bandwith: 20']
   daily_avg_smoothed = []
   daily_avg_smoothed.append(flm.smooth(raw, method='scott', verbose=True))
   daily_avg_smoothed.append(flm.smooth(raw, method='silverman', verbose=True))
   daily_avg_smoothed.append(flm.smooth(raw, method=20))

   data = [go.Scatter(x=daily_avg.index.astype(str),y=daily_avg_smoothed[n], name=names[n+1]) for n in range(0,len(daily_avg_smoothed))]
   data.insert(0,go.Scatter(x=daily_avg.index.astype(str),y=daily_avg,name=names[0]))
   Plot_smooth = go.Figure(data=data,layout=layout)
   Plot_smooth.show()

   # https://ghammad.github.io/pyActigraphy/pyActigraphy-MFDFA.html
   ### (Multi-fractal)Detrended fluctuation analysis
def Multi_fractal(d_folder,d_file,d_start_time,d_period):
      # The DFA methods are part of the Fractal module:
     
      # help(Fractal.dfa)

      fpath = os.path.join(os.path.dirname(fld.__file__),d_folder)
      raw = pyActigraphy.io.read_raw_awd(fpath+d_file, start_time=d_start_time, period=d_period)
      # raw.duration()   Timedelta('9 days 00:01:00')
      # Signal detrending and integration
      profile = Fractal.profile(raw.data.values)

      # Create figure with secondary y-axis
      fig = make_subplots(specs=[[{"secondary_y": True}]])

      # Add traces
      fig.add_trace(
         go.Scatter(x=raw.data.index.astype(str),y=raw.data.values, name='Data'),
         secondary_y=False,
      )
      fig.add_trace(
         go.Scatter(x=raw.data.index.astype(str),y=profile, name='Profile'),
         secondary_y=True,
      )

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
      
      #   DFA
      # In addition to the various functions illustrated above, the pyActigraphy implements a global function that performs all the necessary steps to carry out a DFA analysis:
      # help(Fractal.dfa)
      n_array = np.geomspace(10, 1440, num=50, endpoint=True, dtype=int) # Numbers spaced evenly on a log scale, ranging from an ultradian time scale (10 min.) to a circadian one (1440 min, i.e. 24h)
      # Then, we calculate the associated fluctuations:
      F_n = Fractal.dfa(raw.data,n_array,deg=1)
      fig = go.Figure(data=[go.Scatter(x=n_array,y=np.log(F_n), name='Data fluctuation',mode='markers+lines')])
      fig.update_layout(height=800, width=800,xaxis=dict(title='Time (min.)',type='log'),yaxis=dict(title='log(F(n))'))

      fig.show()

      # Finally, the generalized Hurst exponent can be extracted using:
      Fractal.generalized_hurst_exponent(F_n, n_array, log=False)

      # Multifractal DFA
      # help(Fractal.mfdfa)
      # Let’s now define an array of q values:
      q_array = [1,2,3,4,5,6]
      MF_F_n = Fractal.mfdfa(raw.data,n_array,q_array,deg=1)

      fig = go.Figure(data=[go.Scatter(x=n_array,y=np.log(MF_F_n[:,q]), name='Data fluctuation (q-th order: {})'.format(q_array[q]),mode='markers+lines') for q in range(len(q_array))])
      fig.update_layout(height=800, width=800,xaxis=dict(title='Time (min.)',type='log'),yaxis=dict(title='log(F(n))'))

      fig.show()

      mf_h_q = [Fractal.generalized_hurst_exponent(MF_F_n[:,q],n_array) for q in range(len(q_array))]

# Singular spectrum analysis for time series
def Singular_spectrum_analysis(d_folder,d_File_Formats,d_file,d_start_time,d_period):
  
   # Define the path to your input data
   #fpath = os.path.join(os.path.dirname(fld.__file__),d_folder)
   raw = open_file_by_start_time_period(d_File_Formats,d_file,d_folder,d_start_time, d_period)
   # SSA methodology
   mySSA = SSA(raw.data,window_length='24h')
   # Access the trajectory matrix
   # mySSA.trajectory_matrix().shape   (1440, 11522)
   # Singular value decomposition
   mySSA.fit()

   # Fractional partial variances and Scree diagram
   # By definition, the sum of the partial variances should be equal to 1:
   # mySSA.lambda_s.sum()   1.0

   layout = go.Layout(height=600,width=800,title="Scree diagram",
                        xaxis=dict(title="Singular value index", type='log', showgrid=True, gridwidth=1, gridcolor='LightPink', title_font = {"size": 20}),
                        yaxis=dict(title=r'$\lambda_{k} / \lambda_{tot}$', type='log', showgrid=True, gridwidth=1, gridcolor='LightPink', ), showlegend=False)
   Plot_mySSA = go.Figure(data=[go.Scatter(x=np.arange(0,len(mySSA.lambda_s)+1),y=mySSA.lambda_s)], layout=layout)
   Plot_mySSA.show()

   # Elementary matrices
   x_elem_0 = mySSA.X_elementary(r=0)
   # x_elem_0.shape  (1440, 11522)
   w_corr_mat = mySSA.w_correlation_matrix(10)
   Plot_Elementary_matrices = go.Figure(data=[go.Heatmap(z=w_corr_mat)], layout=go.Layout(height=800,width=800))
   Plot_Elementary_matrices.show()

   # Diagonal averaging
   trend = mySSA.X_tilde(0)
   # By definition, the reconstructed components must have the same dimension as the original signal:
   trend.shape[0] == len(raw.data.index)
   # Rhythmic components (k=1,2)
   et12 = mySSA.X_tilde([1,2])
   # Rhythmic components (k=3,4)
   et34 = mySSA.X_tilde([3,4])
   layout = go.Layout(height=600,width=800, title="", xaxis=dict(title='Date Time'),yaxis=dict(title='Count'),shapes=[],showlegend=True)
   Plot_Diagonal_averaging =go.Figure(data=[
                                             go.Scatter(x=raw.data.index,y=raw.data, name='Activity'),
                                             go.Scatter(x=raw.data.index,y=trend, name='Trend'),
                                             go.Scatter(x=raw.data.index,y=trend+et12, name='Circadian component'),
                                             go.Scatter(x=raw.data.index,y=trend+et34, name='Ultradian component')
                                          ], layout=layout)
   Plot_Diagonal_averaging.show()

   # Compare original signal with its reconstruction
   rec = mySSA.reconstructed_signal([0,1,2,3,4,5,6])
   Plot_reconstructed_signal= go.Figure(data=[  go.Scatter(x=raw.data.index, y=raw.data, name='Activity'),
                                                go.Scatter(x=raw.data.index, y=rec, name='Reconstructed signal')
                                             ], layout=go.Layout(height=600,width=800,showlegend=True))
   Plot_reconstructed_signal.show()












#################################################################
#data(raw)
##Daily_activity_profile(raw)
##Data_Masking(raw)
####Data_Masking_manually(raw,'1918-01-27 09:30:00','1918-01-27 17:48:00')
##Data_Masking_add_mask_periods(raw)
#ok Cleaning_files_individually('awd','data/','example_01.AWD','1918-01-24 08:00:00','9 days')
## Read_a_sleep_diary('data/','example_01.AWD','example_01_sleepdiary.ods','example_01_sleepdiary_extra_states.ods')
#Automatic_detection_of_rest_activity_periods('data/','test_sample_rpx_eng.csv','2015-07-04 12:00:00','6 days','ENG_UK')
#Consolidated_activity_rest_period_detection('data/','SUBJECT_01.AWD')
#Roennebergs_algorithm ('data/','SUBJECT_01.AWD')
#ok Cosinor_analysis('awd','data/','example_01.AWD','1918-01-24 08:30:00',"7D")
# ok Cosinor_analysis('rpx','data/','example.csv','2022-07-24 08:30:00',"7D")
#ok Functional_linear_modelling('awd','data/','example_01.AWD','1918-01-24 08:00:00','9 days')
#Multi_fractal('data/','example_01.AWD','1918-01-24 08:00:00','9 days')
#Singular_spectrum_analysis('data/','awd','example_01.AWD','1918-01-24 08:00:00','9 days')
