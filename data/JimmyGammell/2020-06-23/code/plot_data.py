#%%
# -*- coding: utf-8 -*-

import numpy as np
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import os

output_directory = r'C:\Users\jgamm\Desktop\rssi_measurement\2020-06-23\figures'
locations = ['basement', 'hallway_ii', 'railing_ii']
orientations = ['towards', 'away', 'side']
folder = r'C:/Users/jgamm/Desktop/rssi_measurement/2020-06-23/data'
filenames = ['%1.2f.csv'%(d) for d in np.arange(1, 3.25, .25)]

for location in locations:
    for orientation in orientations:
        fig = make_subplots(rows=2, cols=2,
                            subplot_titles=['Line of sight', 'Blocked'],
                            shared_xaxes = True,
                            specs=[[{'secondary_y': False}, {'secondary_y': False}],
                                   [{'secondary_y': True}, {'secondary_y': True}]])
        rssi_los_hist2d = []
        dist_los_hist2d = []
        times_los = []
        dist_lim = [100, 0]
        db_lim = [-100, 0]
        for filename in filenames:
            data = pd.read_csv(os.path.join(folder, location, '%s_%s'%(orientation, 'los'), filename))
            dists = np.around(data['distance'], 1)
            rssis = data['i_rssi']
            times = data['time_since_start']
            times_los.append(np.mean([times[0]] + [t1-t0 for t0, t1 in zip(times[:-1], times[1:])]))
            for rssi in rssis:
                if rssi-5 < db_lim[1]:
                    db_lim[1] = rssi-5
                if rssi+5 > db_lim[0]:
                    db_lim[0] = rssi+5
            for dist in dists:
                if dist-.5 < dist_lim[0]:
                    dist_lim[0] = dist-.5
                if dist+.5 > dist_lim[1]:
                    dist_lim[1] = dist+.5
            dist_lim[0] = np.max([0, dist_lim[0]])
            column = np.zeros(200)
            hist = np.array(np.unique(rssis, return_counts=True)).T
            for row in hist:
                row_idx = -int(row[0])
                column[row_idx] = row[1]/len(rssis)
            rssi_los_hist2d.append(column)
            column = np.zeros(100)
            hist = np.array(np.unique(dists, return_counts=True)).T
            for row in hist:
                row_idx = int(row[0]/.1)
                column[row_idx] = row[1]/len(dists)
            dist_los_hist2d.append(column)
        rssi_los_hist2d = np.array(rssi_los_hist2d).T
        dist_los_hist2d = np.array(dist_los_hist2d).T
        
        rssi_blocked_hist2d = []
        dist_blocked_hist2d = []
        times_blocked = []
        for filename in filenames:
            data = pd.read_csv(os.path.join(folder, location, '%s_%s'%(orientation, 'blocked'), filename))
            dists = np.around(data['distance'], 1)
            rssis = data['i_rssi']
            times = data['time_since_start']
            times_blocked.append(np.mean([times[0]] + [t1-t0 for t0, t1 in zip(times[:-1], times[1:])]))
            for rssi in rssis:
                if rssi-5 < db_lim[1]:
                    db_lim[1] = rssi-5
                if rssi+5 > db_lim[0]:
                    db_lim[0] = rssi+5
            for dist in dists:
                if dist-.5 < dist_lim[0]:
                    dist_lim[0] = dist-.5
                if dist+.5 > dist_lim[1]:
                    dist_lim[1] = dist+.5
            dist_lim[0] = np.max([0, dist_lim[0]])
            column = np.zeros(200)
            hist = np.array(np.unique(rssis, return_counts=True)).T
            for row in hist:
                row_idx = -int(row[0])
                column[row_idx] = row[1]/len(rssis)
            rssi_blocked_hist2d.append(column)
            column = np.zeros(100)
            hist = np.array(np.unique(dists, return_counts=True)).T
            for row in hist:
                row_idx = int(row[0]/.1)
                column[row_idx] = row[1]/len(dists)
            dist_blocked_hist2d.append(column)
        rssi_blocked_hist2d = np.array(rssi_blocked_hist2d).T
        dist_blocked_hist2d = np.array(dist_blocked_hist2d).T
        
        maxz = np.max([np.max(rssi_blocked_hist2d), np.max(dist_blocked_hist2d),
                       np.max(rssi_los_hist2d), np.max(dist_los_hist2d)])
        fig.add_trace(go.Heatmap(
                        x=np.arange(1, 3.25, .25),
                        y=np.arange(db_lim[0], db_lim[1], -1),
                        z=rssi_los_hist2d[int(-db_lim[0]):int(-db_lim[1]), :],
                        zmin=0, zmax=maxz), row=1, col=1, secondary_y=False)
        fig.add_trace(go.Heatmap(
                        x=np.arange(1, 3.25, .25),
                        y=np.arange(dist_lim[0], dist_lim[1], .1),
                        z=dist_los_hist2d[int(dist_lim[0]/.1):int(dist_lim[1]/.1), :],
                        zmin=0, zmax=maxz), row=2, col=1, secondary_y=False)
        fig.add_trace(go.Heatmap(
                        x=np.arange(1, 3.25, .25),
                        y=np.arange(db_lim[0], db_lim[1], -1),
                        z=rssi_blocked_hist2d[int(-db_lim[0]):int(-db_lim[1]), :],
                        zmin=0, zmax=maxz), row=1, col=2, secondary_y=False)
        fig.add_trace(go.Heatmap(
                        x=np.arange(1, 3.25, .25),
                        y=np.arange(dist_lim[0], dist_lim[1], .1),
                        z=dist_blocked_hist2d[int(dist_lim[0]/.1):int(dist_lim[1]/.1), :],
                        zmin=0, zmax=maxz), row=2, col=2, secondary_y=False)
        fig.add_trace(go.Scatter(
                        x=np.arange(1, 3.25, .25),
                        y=times_los, mode='markers'),
                        row=2, col=1, secondary_y=True)
        fig.add_trace(go.Scatter(
                        x=np.arange(1, 3.25, .25),
                        y=times_blocked, mode='markers'),
                        row=2, col=2, secondary_y=True)
        fig.update_layout(title={'text': 'DA14695 Evaluation Board, %s, %s'%(location, orientation),
                                 'xanchor': 'center', 'yanchor': 'top', 'y': .95, 'x': .5})
        fig.update_xaxes(title='Separation (m)', row=2, col=1)
        fig.update_xaxes(title='Separation (m)', row=2, col=2)
        fig.update_layout(showlegend=False)
        fig.update_yaxes(title_text='Initiator RSSI (dBm)', row=1, col=1, secondary_y=False)
        fig.update_yaxes(title_text='Calculated distance (m)', row=2, col=1, secondary_y=False)
        fig.update_yaxes(title_text='Mean time taken (ms)', row=2, col=1, secondary_y=True)
        fig.update_yaxes(title_text='Mean time taken (ms)', row=2, col=2, secondary_y=True)
        fig.write_image(os.path.join(output_directory, 'distance_%s_%s.png'%(location, orientation)))

