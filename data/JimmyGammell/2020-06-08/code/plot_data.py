#%%
# -*- coding: utf-8 -*-

import numpy as np
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import os

output_directory = r'C:/Users/jgamm/Desktop/rssi_measurement/2020-06-08/figures'
antennas = ['original_whip']
folder = r'C:/Users/jgamm/Desktop/rssi_measurement/2020-06-08/data'
ri_filenames = []
for i_angle in np.arange(0, 360, 45):
    ri_filenames.append('r%di%d.csv'%(i_angle, i_angle))
    ri_filenames.append('r%di%d.csv'%(i_angle+45, i_angle))
ri_filenames.append('r360i360.csv')
angle_filenames = ['%d.csv'%(n) for n in np.arange(0, 405, 45)]
distance_filenames = ['%1.2f.csv'%(n) for n in np.arange(.75, 3.25, .25)]

ref_line = dict(color='white', width=1)

# Plot yaw data
for antenna in antennas:
    fig = make_subplots(rows=2, cols=1,
                        subplot_titles=['Responder RSSI vs. yaw',
                                        'Calculated distance vs. yaw'],
                        shared_xaxes=True)
    rssi_hist2d = []
    dist_hist2d = []
    experiment = 'orientation_exp1'
    dist_lim = [100, 0]
    db_lim = [-100, 0]
    for filename in ri_filenames:
        data = pd.read_csv(os.path.join(folder, antenna, experiment, filename))
        Dist = np.around(data['distance (m)'], 1)
        for rssi in data['reciever RSSI']:
            if rssi-5 < db_lim[1]:
                db_lim[1] = rssi-5
            if rssi+5 > db_lim[0]:
                db_lim[0] = rssi+5
        for dist in Dist:
            if dist-.5 < dist_lim[0]:
                dist_lim[0] = dist-.5
            if dist+.5 > dist_lim[1]:
                dist_lim[1] = dist+.5
        dist_lim[0] = np.max([0, dist_lim[0]])
        column = np.zeros(200)
        hist = np.array(np.unique(data['reciever RSSI'], return_counts=True)).T
        for row in hist:
            row_idx = -int(row[0])
            column[row_idx] = row[1]/len(data['reciever RSSI'])
        rssi_hist2d.append(column)
        column = np.zeros(100)
        hist = np.array(np.unique(Dist, return_counts=True)).T
        for row in hist:
            row_idx = int(np.around(row[0]/.1))
            column[row_idx] = row[1]/len(Dist)
        dist_hist2d.append(column)
    rssi_hist2d = np.array(rssi_hist2d).T
    dist_hist2d = np.array(dist_hist2d).T
    
    maxz = np.max([np.max(rssi_hist2d), np.max(dist_hist2d)])
    fig.add_trace(go.Heatmap(
                    x=np.arange(0, 765, 45),
                    y=np.arange(db_lim[0], db_lim[1], -1),
                    z=rssi_hist2d[int(-db_lim[0]):int(-db_lim[1]), :],
                    zmin=0, zmax=maxz), row=1, col=1)
    fig.add_trace(go.Heatmap(
                    x=np.arange(0, 765, 45),
                    y=np.arange(dist_lim[0], dist_lim[1], .1),
                    z=dist_hist2d[int(dist_lim[0]/.1):int(dist_lim[1]/.1), :],
                    zmin=0, zmax=maxz), row=2, col=1)
    fig.add_trace(go.Scatter(x=np.arange(0, 765, 45), y=np.array([1]*16), mode='lines', line=ref_line), row=2, col=1)
    fig.update_layout(title={'text': 'DA14695 Evaluation Board, %s antenna'%(antenna),
                             'xanchor': 'center', 'yanchor': 'top', 'y': .95, 'x': .5})
    fig.update_xaxes(title='Angle (°)', row=2, col=1)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title_text='Responder RSSI', row=1, col=1)
    fig.update_yaxes(title_text='Calculated distance (m)', row=2, col=1)
    fig.write_image(os.path.join(output_directory, 'orientation_exp1_%s.png'%(antenna)))

# Plot pitch data
for antenna in antennas:
    fig = make_subplots(rows=2, cols=1,
                        subplot_titles=['Responder RSSI vs. pitch',
                                        'Calculated distance vs. pitch'],
                        shared_xaxes=True)
    rssi_hist2d = []
    dist_hist2d = []
    experiment = 'orientation_exp2'
    dist_lim = [100, 0]
    db_lim = [-100, 0]
    for filename in ri_filenames:
        data = pd.read_csv(os.path.join(folder, antenna, experiment, filename))
        Dist = np.around(data['distance (m)'], 1)
        for rssi in data['reciever RSSI']:
            if rssi-5 < db_lim[1]:
                db_lim[1] = rssi-5
            if rssi+5 > db_lim[0]:
                db_lim[0] = rssi+5
        for dist in Dist:
            if dist-.5 < dist_lim[0]:
                dist_lim[0] = dist-.5
            if dist+.5 > dist_lim[1]:
                dist_lim[1] = dist+.5
        dist_lim[0] = np.max([0, dist_lim[0]])
        column = np.zeros(200)
        hist = np.array(np.unique(data['reciever RSSI'], return_counts=True)).T
        for row in hist:
            row_idx = -int(row[0])
            column[row_idx] = row[1]/len(data['reciever RSSI'])
        rssi_hist2d.append(column)
        column = np.zeros(100)
        hist = np.array(np.unique(Dist, return_counts=True)).T
        for row in hist:
            row_idx = int(np.around(row[0]/.1))
            column[row_idx] = row[1]/len(Dist)
        dist_hist2d.append(column)
    rssi_hist2d = np.array(rssi_hist2d).T
    dist_hist2d = np.array(dist_hist2d).T
    
    maxz = np.max([np.max(rssi_hist2d), np.max(dist_hist2d)])
    fig.add_trace(go.Heatmap(
                    x=np.arange(0, 765, 45),
                    y=np.arange(db_lim[0], db_lim[1], -1),
                    z=rssi_hist2d[int(-db_lim[0]):int(-db_lim[1]), :],
                    zmin=0, zmax=maxz), row=1, col=1)
    fig.add_trace(go.Heatmap(
                    x=np.arange(0, 765, 45),
                    y=np.arange(dist_lim[0], dist_lim[1], .1),
                    z=dist_hist2d[int(dist_lim[0]/.1):int(dist_lim[1]/.1), :],
                    zmin=0, zmax=maxz), row=2, col=1)
    fig.add_trace(go.Scatter(x=np.arange(0, 765, 45), y=np.array([1]*16), mode='lines', line=ref_line), row=2, col=1)
    fig.update_layout(title={'text': 'DA14695 Evaluation Board, %s antenna'%(antenna),
                             'xanchor': 'center', 'yanchor': 'top', 'y': .95, 'x': .5})
    fig.update_xaxes(title='Angle (°)', row=2, col=1)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title_text='Responder RSSI', row=1, col=1)
    fig.update_yaxes(title_text='Calculated distance (m)', row=2, col=1)
    fig.write_image(os.path.join(output_directory, 'orientation_exp2_%s.png'%(antenna)))

# Plot roll data
for antenna in antennas:
    fig = make_subplots(rows=2, cols=1,
                        subplot_titles=['Responder RSSI vs. roll',
                                        'Calculated distance vs. roll'],
                        shared_xaxes=True)
    rssi_hist2d = []
    dist_hist2d = []
    experiment = 'orientation_exp3'
    dist_lim = [100, 0]
    db_lim = [-100, 0]
    for filename in ri_filenames:
        data = pd.read_csv(os.path.join(folder, antenna, experiment, filename))
        Dist = np.around(data['distance (m)'], 1)
        for rssi in data['reciever RSSI']:
            if rssi-5 < db_lim[1]:
                db_lim[1] = rssi-5
            if rssi+5 > db_lim[0]:
                db_lim[0] = rssi+5
        for dist in Dist:
            if dist-.5 < dist_lim[0]:
                dist_lim[0] = dist-.5
            if dist+.5 > dist_lim[1]:
                dist_lim[1] = dist+.5
        dist_lim[0] = np.max([0, dist_lim[0]])
        column = np.zeros(200)
        hist = np.array(np.unique(data['reciever RSSI'], return_counts=True)).T
        for row in hist:
            row_idx = -int(row[0])
            column[row_idx] = row[1]/len(data['reciever RSSI'])
        rssi_hist2d.append(column)
        column = np.zeros(100)
        hist = np.array(np.unique(Dist, return_counts=True)).T
        for row in hist:
            row_idx = int(np.around(row[0]/.1))
            column[row_idx] = row[1]/len(Dist)
        dist_hist2d.append(column)
    rssi_hist2d = np.array(rssi_hist2d).T
    dist_hist2d = np.array(dist_hist2d).T
    
    maxz = np.max([np.max(rssi_hist2d), np.max(dist_hist2d)])
    fig.add_trace(go.Heatmap(
                    x=np.arange(0, 765, 45),
                    y=np.arange(db_lim[0], db_lim[1], -1),
                    z=rssi_hist2d[int(-db_lim[0]):int(-db_lim[1]), :],
                    zmin=0, zmax=maxz), row=1, col=1)
    fig.add_trace(go.Heatmap(
                    x=np.arange(0, 765, 45),
                    y=np.arange(dist_lim[0], dist_lim[1], .1),
                    z=dist_hist2d[int(dist_lim[0]/.1):int(dist_lim[1]/.1), :],
                    zmin=0, zmax=maxz), row=2, col=1)
    fig.add_trace(go.Scatter(x=np.arange(0, 765, 45), y=np.array([1]*16), mode='lines', line=ref_line), row=2, col=1)
    fig.update_layout(title={'text': 'DA14695 Evaluation Board, %s antenna'%(antenna),
                             'xanchor': 'center', 'yanchor': 'top', 'y': .95, 'x': .5})
    fig.update_xaxes(title='Angle (°)', row=2, col=1)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title_text='Responder RSSI', row=1, col=1)
    fig.update_yaxes(title_text='Calculated distance (m)', row=2, col=1)
    fig.write_image(os.path.join(output_directory, 'orientation_exp3_%s.png'%(antenna)))

# Plot position data
for antenna in antennas:
    fig = make_subplots(rows=2, cols=1,
                        subplot_titles=['Responder RSSI vs. position',
                                        'Calculated distance vs. position'],
                        shared_xaxes=True)
    rssi_hist2d = []
    dist_hist2d = []
    experiment = 'orientation_exp4'
    dist_lim = [100, 0]
    db_lim = [-100, 0]
    for filename in angle_filenames:
        data = pd.read_csv(os.path.join(folder, antenna, experiment, filename))
        Dist = np.around(data['distance (m)'], 1)
        for rssi in data['reciever RSSI']:
            if rssi-5 < db_lim[1]:
                db_lim[1] = rssi-5
            if rssi+5 > db_lim[0]:
                db_lim[0] = rssi+5
        for dist in Dist:
            if dist-.5 < dist_lim[0]:
                dist_lim[0] = dist-.5
            if dist+.5 > dist_lim[1]:
                dist_lim[1] = dist+.5
        dist_lim[0] = np.max([0, dist_lim[0]])
        column = np.zeros(200)
        hist = np.array(np.unique(data['reciever RSSI'], return_counts=True)).T
        for row in hist:
            row_idx = -int(row[0])
            column[row_idx] = row[1]/len(data['reciever RSSI'])
        rssi_hist2d.append(column)
        column = np.zeros(100)
        hist = np.array(np.unique(Dist, return_counts=True)).T
        for row in hist:
            row_idx = int(np.around(row[0]/.1))
            column[row_idx] = row[1]/len(Dist)
        dist_hist2d.append(column)
    rssi_hist2d = np.array(rssi_hist2d).T
    dist_hist2d = np.array(dist_hist2d).T
    
    maxz = np.max([np.max(rssi_hist2d), np.max(dist_hist2d)])
    fig.add_trace(go.Heatmap(
                    x=np.arange(0, 360, 45),
                    y=np.arange(db_lim[0], db_lim[1], -1),
                    z=rssi_hist2d[int(-db_lim[0]):int(-db_lim[1]), :],
                    zmin=0, zmax=maxz), row=1, col=1)
    fig.add_trace(go.Heatmap(
                    x=np.arange(0, 360, 45),
                    y=np.arange(dist_lim[0], dist_lim[1], .1),
                    z=dist_hist2d[int(dist_lim[0]/.1):int(dist_lim[1]/.1), :],
                    zmin=0, zmax=maxz), row=2, col=1)
    fig.add_trace(go.Scatter(x=np.arange(0, 360, 45), y=np.array([1]*16), mode='lines', line=ref_line), row=2, col=1)
    fig.update_layout(title={'text': 'DA14695 Evaluation Board, %s antenna'%(antenna),
                             'xanchor': 'center', 'yanchor': 'top', 'y': .95, 'x': .5})
    fig.update_xaxes(title='Angle (°)', row=2, col=1)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title_text='Responder RSSI', row=1, col=1)
    fig.update_yaxes(title_text='Calculated distance (m)', row=2, col=1)
    fig.write_image(os.path.join(output_directory, 'orientation_exp4_%s.png'%(antenna)))

# Plot separation data
for antenna in antennas:
    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=['Line of sight', 'Blocked'],
                        shared_xaxes=True)
    rssi_los_hist2d = []
    dist_los_hist2d = []
    experiment = 'distance_los'
    dist_lim = [100, 0]
    db_lim = [-100, 0]
    for filename in distance_filenames:
        data = pd.read_csv(os.path.join(folder, antenna, experiment, filename))
        Dist = np.around(data['distance (m)'], 1)
        for rssi in data['reciever RSSI']:
            if rssi-5 < db_lim[1]:
                db_lim[1] = rssi-5
            if rssi+5 > db_lim[0]:
                db_lim[0] = rssi+5
        for dist in Dist:
            if dist-.5 < dist_lim[0]:
                dist_lim[0] = dist-.5
            if dist+.5 > dist_lim[1]:
                dist_lim[1] = dist+.5
        dist_lim[0] = np.max([0, dist_lim[0]])
        column = np.zeros(200)
        hist = np.array(np.unique(data['reciever RSSI'], return_counts=True)).T
        for row in hist:
            row_idx = -int(row[0])
            column[row_idx] = row[1]/len(data['reciever RSSI'])
        rssi_los_hist2d.append(column)
        column = np.zeros(100)
        hist = np.array(np.unique(Dist, return_counts=True)).T
        for row in hist:
            row_idx = int(np.around(row[0]/.1))
            column[row_idx] = row[1]/len(Dist)
        dist_los_hist2d.append(column)
    rssi_los_hist2d = np.array(rssi_los_hist2d).T
    dist_los_hist2d = np.array(dist_los_hist2d).T
    
    rssi_blocked_hist2d = []
    dist_blocked_hist2d = []
    experiment = 'distance_blocked'
    dist_lim = [100, 0]
    db_lim = [-100, 0]
    for filename in distance_filenames:
        data = pd.read_csv(os.path.join(folder, antenna, experiment, filename))
        Dist = np.around(data['distance (m)'], 1)
        for rssi in data['reciever RSSI']:
            if rssi-5 < db_lim[1]:
                db_lim[1] = rssi-5
            if rssi+5 > db_lim[0]:
                db_lim[0] = rssi+5
        for dist in Dist:
            if dist-.5 < dist_lim[0]:
                dist_lim[0] = dist-.5
            if dist+.5 > dist_lim[1]:
                dist_lim[1] = dist+.5
        dist_lim[0] = np.max([0, dist_lim[0]])
        column = np.zeros(200)
        hist = np.array(np.unique(data['reciever RSSI'], return_counts=True)).T
        for row in hist:
            row_idx = -int(row[0])
            column[row_idx] = row[1]/len(data['reciever RSSI'])
        rssi_blocked_hist2d.append(column)
        column = np.zeros(1000)
        hist = np.array(np.unique(Dist, return_counts=True)).T
        for row in hist:
            row_idx = int(np.around(row[0]/.1))
            column[row_idx] = row[1]/len(Dist)
        dist_blocked_hist2d.append(column)
    rssi_blocked_hist2d = np.array(rssi_blocked_hist2d).T
    dist_blocked_hist2d = np.array(dist_blocked_hist2d).T
    
    maxz = np.max([np.max(rssi_hist2d), np.max(dist_hist2d)])
    fig.add_trace(go.Heatmap(
                    x=np.arange(.75, 3.25, .25),
                    y=np.arange(db_lim[0], db_lim[1], -1),
                    z=rssi_los_hist2d[int(-db_lim[0]):int(-db_lim[1]), :],
                    zmin=0, zmax=maxz), row=1, col=1)
    fig.add_trace(go.Heatmap(
                    x=np.arange(.75, 3.25, .25),
                    y=np.arange(dist_lim[0], dist_lim[1], .1),
                    z=dist_los_hist2d[int(dist_lim[0]/.1):int(dist_lim[1]/.1), :],
                    zmin=0, zmax=maxz), row=2, col=1)
    fig.add_trace(go.Heatmap(
                    x=np.arange(.75, 3.25, .25),
                    y=np.arange(db_lim[0], db_lim[1], -1),
                    z=rssi_blocked_hist2d[int(-db_lim[0]):int(-db_lim[1]), :],
                    zmin=0, zmax=maxz), row=1, col=2)
    fig.add_trace(go.Heatmap(
                    x=np.arange(.75, 3.25, .25),
                    y=np.arange(dist_lim[0], dist_lim[1], .1),
                    z=dist_blocked_hist2d[int(dist_lim[0]/.1):int(dist_lim[1]/.1), :],
                    zmin=0, zmax=maxz), row=2, col=2)
    fig.add_trace(go.Scatter(x=np.arange(.75, 3.25, .25), y=np.arange(.75, 3.25, .25), mode='lines', line=ref_line), row=2, col=1)
    fig.add_trace(go.Scatter(x=np.arange(.75, 3.25, .25), y=np.arange(.75, 3.25, .25), mode='lines', line=ref_line), row=2, col=2)
    fig.update_layout(title={'text': 'DA14695 Evaluation Board, %s antenna'%(antenna),
                             'xanchor': 'center', 'yanchor': 'top', 'y': .95, 'x': .5})
    fig.update_xaxes(title='Separation (m)', row=2, col=1)
    fig.update_xaxes(title='Separation (m)', row=2, col=2)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title_text='Responder RSSI', row=1, col=1)
    fig.update_yaxes(title_text='Calculated distance (m)', row=2, col=1)
    fig.write_image(os.path.join(output_directory, 'distance_%s.png'%(antenna)))