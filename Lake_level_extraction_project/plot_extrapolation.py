from datetime import datetime
from pathlib import Path
import re

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.transforms
import cv2 as cv
from sklearn.metrics import r2_score

DATE_TIME = '%Y-%m-%d %H:%M:%S'

if __name__ == '__main__':
    decrease = pd.read_csv(f"coord_horizontal/decrease/250/lake_level_750_999.csv",
                           parse_dates=["Date Time, GMT-07:00"],
                           date_format=DATE_TIME, na_values='-1')
    decrease.dropna(inplace=True)
    decrease["Date Time, GMT-07:00"] = decrease["Date Time, GMT-07:00"].dt.round("H")
    decrease_observed = decrease[decrease["Date Time, GMT-07:00"] <= datetime.strptime('2023-06-16 12:00:00', DATE_TIME)]
    decrease_extrapolate = decrease[decrease["Date Time, GMT-07:00"] > datetime.strptime('2023-06-16 12:00:00', DATE_TIME)]
    pressure_df = pd.read_csv("Lake_air_pressure.csv", parse_dates=["Date Time, GMT-07:00"], date_format=DATE_TIME)
    decrease_observed = pd.merge(decrease_observed, pressure_df, on="Date Time, GMT-07:00")
    transfer_function = [0.049755, -100.337164, 2018.8012920598198 - 1997.6460330645627]
    transfer_function1 = [0.054009, -108.346527]
    transfer_function2 = [0.073607, -147.888208]
    transfer_function3 = [0.049818, -99.411562]
    transfer_function4 = [0.050894, -101.614759]
    decrease_extrapolate['extrapolate_depth'] = transfer_function[0] * (decrease_extrapolate.y + transfer_function[2]) + transfer_function[1]
    decrease_extrapolate['extrapolate_depth_1'] = transfer_function1[0] * decrease_extrapolate.y + transfer_function1[1]
    decrease_extrapolate['extrapolate_depth_2'] = transfer_function2[0] * decrease_extrapolate.y + transfer_function2[1]
    decrease_extrapolate['extrapolate_depth_3'] = transfer_function3[0] * decrease_extrapolate.y + transfer_function3[1]
    decrease_extrapolate['extrapolate_depth_4'] = transfer_function4[0] * decrease_extrapolate.y + transfer_function4[1]
    funct_label = f'\ny = {transfer_function[0]} * (x + {transfer_function[2]}) + {transfer_function[1]}'
    funct_label_1 = f'\ny = {transfer_function1[0]} * x + {transfer_function1[1]}'
    funct_label_2 = f'\ny = {transfer_function2[0]} * x + {transfer_function2[1]}'
    funct_label_3 = f'\ny = {transfer_function3[0]} * x + {transfer_function3[1]}'
    funct_label_4 = f'\ny = {transfer_function4[0]} * x + {transfer_function4[1]}'
    fig = plt.figure(figsize=(12, 10))
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes = plt.gca()
    plt.plot(decrease_observed['y'], decrease_observed['Lake depth (m)'],
             label='Observed data', color='b', marker='o', linestyle='dashed')
    plt.plot(decrease_extrapolate['y'], decrease_extrapolate['extrapolate_depth'],
             label=f'Extrapolated data using increase function{funct_label}', color='c', marker='o', linestyle='dashed',
             markersize=8, markerfacecolor='none')
    plt.plot(decrease_extrapolate['y'], decrease_extrapolate['extrapolate_depth_4'],
             label=f'Extrapolated data using decrease function{funct_label_4}', color='tab:pink', marker='o', linestyle='dashed',
             markersize=8, markerfacecolor='none')
    plt.plot(decrease_extrapolate['y'], decrease_extrapolate['extrapolate_depth_1'],
             label=f'Extrapolated data using decrease upper function{funct_label_1}', color='y', marker='o', linestyle='dashed',
             markersize=8, markerfacecolor='none')
    plt.plot(decrease_extrapolate['y'], decrease_extrapolate['extrapolate_depth_2'],
             label=f'Extrapolated data using decrease lower function{funct_label_2}', color='m', marker='o', linestyle='dashed',
             markersize=8, markerfacecolor='none')
    plt.plot(decrease_extrapolate['y'], decrease_extrapolate['extrapolate_depth_3'],
             label=f'Extrapolated data using combine function{funct_label_3}', color='tab:brown', marker='+', linestyle='dashed',
             markersize=8)
    axes.xaxis.set_major_locator(ticker.MultipleLocator(50))
    axes.yaxis.set_major_locator(ticker.MultipleLocator(2.5))
    axes.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    axes.yaxis.set_minor_locator(ticker.MultipleLocator(0.5))
    axes.tick_params(axis='y', which='major', labelsize=14)
    axes.tick_params(axis='x', which='major', labelsize=14)
    axes.set_xlabel("Pixelated water level (px)", fontsize=16)
    axes.set_ylabel("Water level relative to pressure sensor (m)", fontsize=16)
    axes.legend(fontsize=14)
    axes.set_title(f"Scatter plot of Pixelated water level vs water level using segmented profile"
                   f" 750-999\n"
                   "from 2023-06-15 15:00:00 to 2023-06-17 05:00:00", fontsize=18)
    plt.savefig(f"plot_result/extrapolation/scatter_extrapolate.png", bbox_inches='tight')

    fig = plt.figure(figsize=(12, 10))
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes = plt.gca()
    plt.plot(decrease_observed['Date Time, GMT-07:00'], decrease_observed['Lake depth (m)'],
                label='Observed data', color='b', marker='o', linestyle='dashed')
    plt.plot(decrease_extrapolate['Date Time, GMT-07:00'], decrease_extrapolate['extrapolate_depth'],
                label=f'Extrapolated data using increase function{funct_label}', color='c', marker='o', linestyle='dashed',
             markersize=8, markerfacecolor='none')
    plt.plot(decrease_extrapolate['Date Time, GMT-07:00'], decrease_extrapolate['extrapolate_depth_4'],
             label=f'Extrapolated data using decrease function{funct_label_4}', color='tab:pink', marker='o', linestyle='dashed',
             markersize=8, markerfacecolor='none')
    plt.plot(decrease_extrapolate['Date Time, GMT-07:00'], decrease_extrapolate['extrapolate_depth_1'],
                label=f'Extrapolated data using decrease upper function{funct_label_2}', color='y', marker='o', linestyle='dashed',
             markersize=8, markerfacecolor='none')
    plt.plot(decrease_extrapolate['Date Time, GMT-07:00'], decrease_extrapolate['extrapolate_depth_2'],
                label=f'Extrapolated data using decrease lower function{funct_label_2}', color='m', marker='o', linestyle='dashed',
             markersize=8, markerfacecolor='none')
    plt.plot(decrease_extrapolate['Date Time, GMT-07:00'], decrease_extrapolate['extrapolate_depth_3'],
             label=f'Extrapolated data using combine function{funct_label_3}', color='tab:brown', marker='+', linestyle='dashed',
             markersize=8, markerfacecolor='none')
    axes.legend(fontsize=14)
    axes.set_ylabel("Water level relative to pressure sensor (m)", fontsize=16)
    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))

    dx = 0 / 72.
    dy = -15 / 72.
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)
    for label in axes.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)

    axes.xaxis.set_major_locator(mdates.DayLocator())
    axes.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
    axes.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 2)))
    axes.yaxis.set_major_locator(ticker.MultipleLocator(2.5))
    axes.yaxis.set_minor_locator(ticker.MultipleLocator(0.5))
    axes.tick_params(axis='y', which='major', labelsize=14)
    axes.tick_params(axis='x', which='both', labelsize=14)
    axes.set_title(f"Time series plot of water depth using segmented profile"
                   f" 750-999\n"
                   "from 2023-06-15 15:00:00 to 2023-06-17 05:00:00", fontsize=18)
    plt.savefig(f"plot_result/extrapolation/ts_extrapolate.png", bbox_inches='tight')

