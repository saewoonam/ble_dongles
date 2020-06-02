#%%
# -*- coding: utf-8 -*-

import numpy as np
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import os

output_directory = r'C:/Users/jgamm/Desktop/rssi_measurement/2020-06-01/figures'
antennas = ['coil', 'dome', 'pcb']
folder = r'C:/Users/jgamm/Desktop/rssi_measurement/2020-06-01'
rxtx_filenames = []
for tx_angle in np.arange(0, 360, 45):
    rxtx_filenames.append('rx%dtx%d.csv'%(tx_angle, tx_angle))
    rxtx_filenames.append('rx%dtx%d.csv'%(tx_angle+45, tx_angle))
rxtx_filenames.append('rx360tx360.csv')
angle_filenames = ['%d.csv'%(n) for n in np.arange(0, 405, 45)]
distance_filenames = ['%1.2f.csv'%(d) for d in np.arange(.75, 3.25, .25)]

def load_data(filename):
    data = pd.read_csv(filename)
    return data

# Plot yaw data
experiment = 'orientation_exp1'
for antenna in antennas:
    fig = make_subplots(rows=1, cols=1)
    hist2d = []
    db_lim = [-100, 0]
    for filename in rxtx_filenames:
        data = pd.read_csv(os.path.join(folder, antenna, experiment, filename))
        for rssi in data['RSSI (dB)']:
            if rssi-5 < db_lim[1]:
                db_lim[1] = rssi-5
            if rssi+5 > db_lim[0]:
                db_lim[0] = rssi+5
        column = np.zeros(200)
        hist = np.array(np.unique(data['RSSI (dB)'], return_counts=True)).T
        for row in hist:
            row_idx = -int(row[0]/.5)
            column[row_idx] = row[1]/len(data['RSSI (dB)'])
        hist2d.append(column)
    hist2d = np.array(hist2d).T
    fig.add_trace(go.Heatmap(
                  x=np.arange(0, 765, 45),
                  y=np.arange(db_lim[0], db_lim[1], -.5),
                  z=hist2d[int(-2*db_lim[0]):int(-2*db_lim[1]), :]), row=1, col=1)
    fig.update_layout(title={'text': 'RFM69HCW at 915MHz, RSSI vs. yaw, %s antenna'%(antenna), 'xanchor': 'center',
                             'yanchor': 'top', 'y': .95, 'x': .5},
                      yaxis_title='Normalized histogram of RSSI (dBm)',
                      xaxis_title='Angle (°)')
    fig.write_image(os.path.join(output_directory, '%s_%s.png'%(experiment, antenna)))

# Plot pitch data
experiment = 'orientation_exp2'
for antenna in antennas:
    fig = make_subplots(rows=1, cols=1)
    hist2d = []
    db_lim = [-100, 0]
    for filename in rxtx_filenames:
        data = pd.read_csv(os.path.join(folder, antenna, experiment, filename))
        for rssi in data['RSSI (dB)']:
            if rssi-5 < db_lim[1]:
                db_lim[1] = rssi-5
            if rssi+5 > db_lim[0]:
                db_lim[0] = rssi+5
        column = np.zeros(200)
        hist = np.array(np.unique(data['RSSI (dB)'], return_counts=True)).T
        for row in hist:
            row_idx = -int(row[0]/.5)
            column[row_idx] = row[1]/len(data['RSSI (dB)'])
        hist2d.append(column)
    hist2d = np.array(hist2d).T
    fig.add_trace(go.Heatmap(
                  x=np.arange(0, 765, 45),
                  y=np.arange(db_lim[0], db_lim[1], -.5),
                  z=hist2d[int(-2*db_lim[0]):int(-2*db_lim[1]), :]), row=1, col=1)
    fig.update_layout(title={'text': 'RFM69HCW at 915MHz, RSSI vs. pitch, %s antenna'%(antenna), 'xanchor': 'center',
                             'yanchor': 'top', 'y': .95, 'x': .5},
                      yaxis_title='Normalized histogram of RSSI (dBm)',
                      xaxis_title='Angle (°)')
    fig.write_image(os.path.join(output_directory, '%s_%s.png'%(experiment, antenna)))

# Plot roll data
experiment = 'orientation_exp3'
for antenna in antennas:
    fig = make_subplots(rows=1, cols=1)
    hist2d = []
    db_lim = [-100, 0]
    for filename in rxtx_filenames:
        data = pd.read_csv(os.path.join(folder, antenna, experiment, filename))
        for rssi in data['RSSI (dB)']:
            if rssi-5 < db_lim[1]:
                db_lim[1] = rssi-5
            if rssi+5 > db_lim[0]:
                db_lim[0] = rssi+5
        column = np.zeros(200)
        hist = np.array(np.unique(data['RSSI (dB)'], return_counts=True)).T
        for row in hist:
            row_idx = -int(row[0]/.5)
            column[row_idx] = row[1]/len(data['RSSI (dB)'])
        hist2d.append(column)
    hist2d = np.array(hist2d).T
    fig.add_trace(go.Heatmap(
                  x=np.arange(0, 765, 45),
                  y=np.arange(db_lim[0], db_lim[1], -.5),
                  z=hist2d[int(-2*db_lim[0]):int(-2*db_lim[1]), :]), row=1, col=1)
    fig.update_layout(title={'text': 'RFM69HCW at 915MHz, RSSI vs. roll, %s antenna'%(antenna), 'xanchor': 'center',
                             'yanchor': 'top', 'y': .95, 'x': .5},
                      yaxis_title='Normalized histogram of RSSI (dBm)',
                      xaxis_title='Angle (°)')
    fig.write_image(os.path.join(output_directory, '%s_%s.png'%(experiment, antenna)))

# Plot position data
experiment = 'orientation_exp4'
for antenna in antennas:
    fig = make_subplots(rows=1, cols=1)
    hist2d = []
    db_lim = [-100, 0]
    for filename in angle_filenames:
        data = pd.read_csv(os.path.join(folder, antenna, experiment, filename))
        for rssi in data['RSSI (dB)']:
            if rssi-5 < db_lim[1]:
                db_lim[1] = rssi-5
            if rssi+5 > db_lim[0]:
                db_lim[0] = rssi+5
        column = np.zeros(200)
        hist = np.array(np.unique(data['RSSI (dB)'], return_counts=True)).T
        for row in hist:
            row_idx = -int(row[0]/.5)
            column[row_idx] = row[1]/len(data['RSSI (dB)'])
        hist2d.append(column)
    hist2d = np.array(hist2d).T
    fig.add_trace(go.Heatmap(
                  x=np.arange(0, 765, 45),
                  y=np.arange(db_lim[0], db_lim[1], -.5),
                  z=hist2d[int(-2*db_lim[0]):int(-2*db_lim[1]), :]), row=1, col=1)
    fig.update_layout(title={'text': 'RFM69HCW at 915MHz, RSSI vs. position, %s antenna'%(antenna), 'xanchor': 'center',
                             'yanchor': 'top', 'y': .95, 'x': .5},
                      yaxis_title='Normalized histogram of RSSI (dBm)',
                      xaxis_title='Angle (°)')
    fig.write_image(os.path.join(output_directory, '%s_%s.png'%(experiment, antenna)))

# Plot separation data
for antenna in antennas:
    fig = make_subplots(rows=1, cols=2, subplot_titles=['Line of sight', 'Blocked by water jug'], shared_yaxes=True)
    los_hist2d = []
    experiment = 'distance_los'
    db_lim = [-100, 0]
    for filename in distance_filenames:
        data = pd.read_csv(os.path.join(folder, antenna, experiment, filename))
        for rssi in data['RSSI (dB)']:
            if rssi-5 < db_lim[1]:
                db_lim[1] = rssi-5
            if rssi+5 > db_lim[0]:
                db_lim[0] = rssi+5
        column = np.zeros(200)
        hist = np.array(np.unique(data['RSSI (dB)'], return_counts=True)).T
        for row in hist:
            row_idx = -int(row[0]/.5)
            column[row_idx] = row[1]/len(data['RSSI (dB)'])
        los_hist2d.append(column)
    los_hist2d = np.array(los_hist2d).T
    
    blocked_hist2d = []
    experiment = 'distance_blocked'
    for filename in distance_filenames:
        data = pd.read_csv(os.path.join(folder, antenna, experiment, filename))
        for rssi in data['RSSI (dB)']:
            if rssi-5 < db_lim[1]:
                db_lim[1] = rssi-5
            if rssi+5 > db_lim[0]:
                db_lim[0] = rssi+5
        column = np.zeros(200)
        hist = np.array(np.unique(data['RSSI (dB)'], return_counts=True)).T
        for row in hist:
            row_idx = -int(row[0]/.5)
            column[row_idx] = row[1]/len(data['RSSI (dB)'])
        blocked_hist2d.append(column)
    blocked_hist2d = np.array(blocked_hist2d).T
    
    maxz = np.max([np.max(los_hist2d), np.max(blocked_hist2d)])
    fig.add_trace(go.Heatmap(
            x=np.arange(.75, 3.25, .25),
            y=np.arange(db_lim[0], db_lim[1], -.5),
            z=los_hist2d[int(-2*db_lim[0]):int(-2*db_lim[1]), :], zmin=0, zmax=maxz), row=1, col=1)
    fig.add_trace(go.Heatmap(
                  x=np.arange(.75, 3.25, .25),
                  y=np.arange(db_lim[0], db_lim[1], -.5),
                  z=blocked_hist2d[int(-2*db_lim[0]):int(-2*db_lim[1]), :], zmin=0, zmax=maxz), row=1, col=2)
    fig.update_layout(title={'text': 'RFM69HCW at 915MHz, RSSI vs. position, %s antenna'%(antenna), 'xanchor': 'center',
                         'yanchor': 'top', 'y': .95, 'x': .5},
                      yaxis_title='Normalized histogram of RSSI (dBm)')
    fig.update_xaxes(title_text='Separation (m)', row=1, col=1)
    fig.update_xaxes(title_text='Separation (m)', row=1, col=2)
    fig.write_image(os.path.join(output_directory, 'distance_%s.png'%(antenna)))