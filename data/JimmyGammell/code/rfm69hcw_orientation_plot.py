#%%
# -*- coding: utf-8 -*-

# Purpose of script:
#   Plot histogram of RFM69HCW RSSI for varying angle between antennae.
# How to use:
#   (filepath)/(experiment) is folder containing one CSV file for each trial.
#   Trials should be named '%ddeg'%(angle) where angle gives the angle in degrees
#    between receiver and transmitter antennae.
#   Code expects a trial for angles 0, 45, 90, ..., 360 degrees.
#   db_lim determines y-axis range - db_lim[0] is high value and db_lim[1] is low value.
#   antenna_name determines name that will be displayed in graph title.

filepath = r'C:/Users/jgamm/Desktop/rssi_measurement/data/orientation/rfm69hcw/pcb'
experiment = r'exp_3/csv'
db_lim = [-20, -30] # Range of y-axis
antenna_name = 'PCB trace antenna'

import numpy as np
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import os

def load_data(filename):
    Data = pd.read_csv(filename)
    return Data

# Expected 

filenames = []
for angle in np.arange(0, 405, 45):
    filenames.append(r'%ddeg.csv'%(angle))

fig = make_subplots(rows=1, cols=1, shared_yaxes=True)


hist2d = []
for file in filenames:
    data = load_data(os.path.join(filepath, experiment, file))
    column = np.zeros(250)
    hist = np.array(np.unique(data['RSSI'], return_counts=True)).T
    for row in hist:
        row_idx = -int(row[0]/.5)
        column[row_idx] = row[1]/len(data['RSSI'])
    hist2d.append(column)
hist2d = np.array(hist2d).T
fig.add_trace(go.Heatmap(
                x=np.arange(0, 405, 45),
                y=np.arange(db_lim[0], db_lim[1], -.5),
                z=hist2d[-2*db_lim[0]:-2*db_lim[1], :], zmin=0, zmax=.6), row=1, col=1)

fig.update_layout(title={'text': 'RFM69HCW at 915MHz, %s'%(antenna_name), 'xanchor': 'center', 'yanchor': 'top', 'y':.95, 'x':.5},
                  yaxis_title='Normalized histogram of RSSI (dBm)')
                  
fig.update_xaxes(title_text='Angle (°)', row=1, col=1)
    
plotly.offline.plot(fig)