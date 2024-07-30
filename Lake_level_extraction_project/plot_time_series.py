import re
from pathlib import Path
from plot_scatter import DECREASE_PERIOD, INCREASE_PERIOD, YEAR_2022_PEROD

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.transforms
import glob

DATE_TIME = '%Y-%m-%d %H:%M:%S'


def plot_time_series(date_time, pixel_level, profile, period, num_profiles):
    if period == '2022':
        fig = plt.figure(figsize=(16, 10))
    else:
        fig = plt.figure(figsize=(12, 10))

    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes = plt.gca()
    axes.plot(date_time, pixel_level, marker='.', linestyle='-')
    if period == '2022':
        axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    else:
        axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))

    dx = 0 / 72.
    dy = -15 / 72.
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)
    for label in axes.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)

    axes.xaxis.set_major_locator(mdates.DayLocator())
    axes.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
    if period == 'decrease':
        axes.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 2)))
        axes.yaxis.set_major_locator(ticker.MultipleLocator(50))
        axes.yaxis.set_minor_locator(ticker.MultipleLocator(5))
        period_text = DECREASE_PERIOD
        axes.tick_params(axis='x', which='minor', labelsize=14)
    elif period == 'increase':
        axes.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 4)))
        axes.yaxis.set_major_locator(ticker.MultipleLocator(10))
        axes.yaxis.set_minor_locator(ticker.MultipleLocator(1))
        period_text = INCREASE_PERIOD
        axes.tick_params(axis='x', which='minor', labelsize=14)
    elif period == '2022':
        axes.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 8)))
        axes.yaxis.set_major_locator(ticker.MultipleLocator(50))
        axes.yaxis.set_minor_locator(ticker.MultipleLocator(5))
        period_text = YEAR_2022_PEROD

    axes.tick_params(axis='both', which='major', labelsize=14)
    axes.set_ylabel("Pixelated water level (px)", fontsize=16)
    axes.set_title(f"Time series plot of Pixelated water level using segmented profile"
                   f" {profile[0]}-{profile[1]}\n"
                   f"{period_text}", fontsize=18)
    plt.savefig(f'plot_result/time_series/{period}/{num_profiles}/tsplot_{profile[0]}_{profile[1]}.png', bbox_inches='tight')
    plt.close(fig)


def plot_all_time_series(period, num_profiles):
    data_dirs = glob.glob(f'coord_horizontal/{period}/{num_profiles}/*.csv')
    for data_dir in data_dirs:
        data_name = Path(data_dir).stem
        profile = re.findall(r'\d+', data_name)
        data_df = pd.read_csv(data_dir, parse_dates=["Date Time, GMT-07:00"], date_format=DATE_TIME, na_values='-1')
        data_df = data_df.dropna()
        data_df["Date Time, GMT-07:00"] = data_df["Date Time, GMT-07:00"].dt.round("h")
        plot_time_series(data_df["Date Time, GMT-07:00"], data_df["y"].astype(np.int64), profile, period, num_profiles)


if __name__ == '__main__':
    plot_all_time_series("decrease", 250)
    plot_all_time_series("decrease", 350)
    plot_all_time_series("increase", 250)
    plot_all_time_series("increase", 350)
    plot_all_time_series("2022", 300)
