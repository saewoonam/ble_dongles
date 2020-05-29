#%%
# -*- coding: utf-8 -*-

# Purpose of script:
#   Plot histogram of BLE modules RSSI over varying distance.
#   Adjacent subplots - line-of-sight data on left, and obstructed by water jug
#    on right.
#   Also plots proportion of packets that were received from each channel, for
#    each distance.
# How to use:
#   filepath gives folder where data is contained.
#   Data format: one CSV file for each trial.
#   Trials should be named '%1.2f_%s'%(distance, setup) where distance is separation
#    between modules (m) and setup is 'los' if modules had an unobstructed line of sight,
#    and 'blocked' if there was a jug of water between them.
#   Code expects a trial for both setups for distances 0.50, 0.75, ..., 3.00.
#   channel determines which channel (37, 38, or 39) will be plotted.
#   db_lim determines y-axis range - db_lim[0] is high value and db_lim[1] is low value.

filepath = r'C:/Users/jgamm/Desktop/rssi_measurement/data/bluetooth_outdoors'
channel = 39 #37, 38 or 39
db_lim = [-45, -85]

import numpy as np
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import os

def load_data(filename):
    Data = pd.read_csv(filename)
    return Data


num_transmissions = {'los':{37: [0]*11, 38: [0]*11, 39: [0]*11},
                     'blocked':{37: [0]*11, 38: [0]*11, 39: [0]*11}}

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
for j, file in zip(range(11), los_filenames):
    data = load_data(os.path.join(filepath, file))
    rssi = []
    for i in range(len(data[' rssi'])):
        num_transmissions['los'][data[' channel'][i]][j] += 1
        if data[' channel'][i] == channel:
            rssi.append(data[' rssi'][i])
    column = np.zeros(250)
    hist = np.array(np.unique(rssi, return_counts=True)).T
    for row in hist:
        row_idx = -int(row[0]/.5)
        column[row_idx] = row[1]/len(rssi)
    hist2d.append(column)
hist2d = np.array(hist2d).T
fig.add_trace(go.Heatmap(
                x=np.arange(.5, 3.5, .25),
                y=np.arange(db_lim[0], db_lim[1], -.5),
                z=hist2d[-2*db_lim[0]:-2*db_lim[1], :], zmin=0, zmax=.6), row=1, col=1)

hist2d = []
for j, file in zip(range(11), blocked_filenames):
    data = load_data(os.path.join(filepath, file))
    rssi = []
    for i in range(len(data[' rssi'])):
        num_transmissions['blocked'][data[' channel'][i]][j] += 1
        if data[' channel'][i] == channel:
            rssi.append(data[' rssi'][i])
    column = np.zeros(250)
    hist = np.array(np.unique(rssi, return_counts=True)).T
    for row in hist:
        row_idx = -int(row[0]/.5)
        column[row_idx] = row[1]/len(rssi)
    hist2d.append(column)
hist2d = np.array(hist2d).T
fig.add_trace(go.Heatmap(
                x=np.arange(.5, 3.5, .25),
                y=np.arange(db_lim[0], db_lim[1], -.5),
                z=hist2d[-2*db_lim[0]:-2*db_lim[1], :], zmin=0, zmax=.6), row=1, col=2)

fig.update_layout(title={'text': 'Bluetooth dongles, channel %d'%(channel), 'xanchor': 'center', 'yanchor': 'top', 'y':.95, 'x':.5},
                  yaxis_title='Normalized histogram of RSSI (dB)')
                  
fig.update_xaxes(title_text='Separation (m)', row=1, col=1)
fig.update_xaxes(title_text='Separation (m)', row=1, col=2)
    
plotly.offline.plot(fig)

colors = {37: 'blue', 38: 'green', 39: 'red'}
fig, (ax0, ax1) = plt.subplots(1, 2, sharey=True)
for channel in [37, 38, 39]:
    ax0.plot(np.arange(.5, 3.25, .25), [val/250 for val in num_transmissions['los'][channel]], '-', color=colors[channel])
    ax1.plot(np.arange(.5, 3.25, .25), [val/250 for val in num_transmissions['blocked'][channel]], '-', color=colors[channel], label='Channel %d'%(channel))
ax0.set_title('Line of sight')
ax1.set_title('Blocked')
ax0.set_xlabel('Separation (m)')
ax1.set_xlabel('Separation (m)')
ax0.set_ylabel('Proportion of packets received')
ax1.legend()
fig.suptitle('Proportion of packets received from each channel')