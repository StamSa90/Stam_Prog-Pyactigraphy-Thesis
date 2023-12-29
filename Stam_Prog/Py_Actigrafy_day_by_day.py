import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import Py_actigrafi_app as Py
from datetime import datetime


def Actigrafy_day_by_day(p_File_Formats,p_folder,p_file,p_start__time,p_period):
       
       
        txt = p_period
        p_period_0 ="0 "+txt[txt.find(' ')+1:len(txt)]

        num_days =int(txt[0:txt.find(' ')])
        #print (days)
        # Create subplots
        fig = make_subplots(rows=num_days+1, cols=1)   #, subplot_titles=['Day 1', 'Day 2']
        #print (txt[0:txt.find(' ')]  +"ggg"+txt[txt.find(' ')+1:len(txt)])
        p_start_time=[]
        raws=[]
        x=[]
        y=[]
        trace=[]
        trace_ck=[]
        for i in range(num_days+1):
                print(i)
                datetime_object = datetime.strptime(p_start__time, '%Y-%m-%d %H:%M:%S')+ timedelta(days=i)

                p_start_time.append(str(datetime_object))
                    
                raw = Py.open_file_by_start_time_period(p_File_Formats,p_file,p_folder, p_start_time[i], p_period_0)
                        
                raws.append(raw)
                x.append(raw.data.index.astype(str))
                y.append(raw.data)
                CK = raw.CK()
                    # Add traces to the subplot
                trace.append(go.Scatter(x=x[i], y=y[i], mode='lines+markers', name=p_start_time[i]))
            #####  CK
            #  trace_ck.append(go.Scatter(x=CK.index.astype(str),y=CK, yaxis='y2', name='CK '+p_start_time[i]))

            # CK = raw.CK()
            # layout = go.Layout(title="Rest/Activity detection",xaxis=dict(title="Date time"), yaxis=dict(title="Counts/period"), showlegend=False)
            # layout.update(yaxis2=dict(title='Classification',overlaying='y',side='right'), showlegend=True);
                
                #Cole_Kripke = go.Figure(data=[ go.Scatter(x=raw.data.index.astype(str),y=raw.data, name='Data'), 
                #                               go.Scatter(x=CK.index.astype(str),y=CK, yaxis='y2', name='CK')], layout=layout)
            # Cole_Kripke.show()
                

                fig.add_trace(trace[i], row=i+1, col=1)
            


        # Update layout
        fig.update_layout(
            title="Actigraphy data",
            yaxis=dict(title="Counts/period"),
            showlegend=True,
            hovermode='closest',
            autosize=False,
            width=1200,
            height=1200,
        )
        fig.update_yaxes(automargin=True)

        # Show the plot
        fig.show()
 # Sample data for demonstration
#p_File_Formats = 'rpx'
#p_file = 'example.csv'
#p_folder = 'data/'
#p_start_time = "2022-07-18 13:00:00"
#p_period ="6 days 23:59:45"
#Actigrafy_day_by_day(p_File_Formats,p_file,p_folder,p_start_time,p_period)