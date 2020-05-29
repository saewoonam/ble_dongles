#%%
# -*- coding: utf-8 -*-

# Purpose of script:
#   Plot histogram of RFM69HCW RSSI over varying distance.
#   Adjacent subplots - line-of-sight data on left, and obstructed by water jug
#    on right.
# How to use:
#   (filepath)/(experiment) is folder containing one CSV file for each trial.
#   Trials should be named '%1.2f_%s'%(distance, setup) where distance is separation
#    (m) between radios and setup is 'los' if radios had an unobstructed line of sight,
#    and 'blocked' if there was a jug of water between them.
#   Code expects a trial for both setups for distances 0.50, 0.75, ..., 3.00.
#   db_lim determines y-axis range - db_lim[0] is high value and db_lim[1] is low value.
#   antenna_name determines name that will be displayed in graph title.

filepath = r'C:/Users/jgamm/Desktop/rssi_measurement/data'
experiment = r'rfm69hcw_qwa_outdoors/csv'
db_lim = [-20, -60] # Range of y-axis
antenna_name = 'quarter-wavelength wire antenna'

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

los_filenames = []
for distance in np.arange(.5, 3.25, .25):
    filename = '%1.2f_los.csv'%(distance)
    los_filenames.append(filename)
blocked_filenames = []
for distance in np.arange(.5, 3.25, .25):
    filename = '%1.2f_blocked.csv'%(distance)
    blocked_filenames.append(filename)

fig = make_subplots(rows=1, cols=2, subplot_titles=['Line of sight', 'Blocked by water jug'], shared_yaxes=True)


hist2d = []
for file in los_filenames:
    data = load_data(os.path.join(filepath, experiment, file))
    column = np.zeros(250)
    hist = np.array(np.unique(data['RSSI'], return_counts=True)).T
    for row in hist:
        row_idx = -int(row[0]/.5)
        column[row_idx] = row[1]/len(data['RSSI'])
    hist2d.append(column)
hist2d = np.array(hist2d).T
fig.add_trace(go.Heatmap(
                x=np.arange(.5, 3.5, .25),
                y=np.arange(db_lim[0], db_lim[1], -.5),
                z=hist2d[-2*db_lim[0]:-2*db_lim[1], :], zmin=0, zmax=.6), row=1, col=1)

hist2d = []
for file in blocked_filenames:
    data = load_data(os.path.join(filepath, experiment, file))
    column = np.zeros(250)
    hist = np.array(np.unique(data['RSSI'], return_counts=True)).T
    for row in hist:
        row_idx = -int(row[0]/.5)
        column[row_idx] = row[1]/len(data['RSSI'])
    hist2d.append(column)
hist2d = np.array(hist2d).T
fig.add_trace(go.Heatmap(
                x=np.arange(.5, 3.5, .25),
                y=np.arange(db_lim[0], db_lim[1], -.5),
                z=hist2d[-2*db_lim[0]:-2*db_lim[1], :], zmin=0, zmax=.6), row=1, col=2)

fig.update_layout(title={'text': 'RFM69HCW at 915MHz, %s'%(antenna_name), 'xanchor': 'center', 'yanchor': 'top', 'y':.95, 'x':.5},
                  yaxis_title='Normalized histogram of RSSI (dBm)')
                  
fig.update_xaxes(title_text='Separation (m)', row=1, col=1)
fig.update_xaxes(title_text='Separation (m)', row=1, col=2)
    
plotly.offline.plot(fig)