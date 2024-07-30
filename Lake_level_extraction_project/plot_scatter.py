from datetime import datetime
from pathlib import Path
import re

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import glob

DATE_TIME = '%Y-%m-%d %H:%M:%S'
DECREASE_PERIOD = "from 2023-06-15 15:00:00 to 2023-06-16 12:00:00"
DECREASE_PERIOD_NO_CUTOFF = "from 2023-06-15 15:00:00 to 2023-06-17 05:00:00"
INCREASE_PERIOD = "from 2023-05-31 15:00:00 to 2023-06-05 23:00:00"
YEAR_2022_PEROD = "from 2022-07-23 04:00:00 to 2022-08-11 03:00:00"


def plot_scatter_raw(pressure, period, num_profiles):
    data_dirs = glob.glob(f'coord_horizontal/{period}/{num_profiles}/*.csv')
    profiles = []
    r_scores = []
    for data_dir in data_dirs:
        data_name = Path(data_dir).stem
        profile = re.findall(r'\d+', data_name)
        profiles.append(f"{profile[0]}-{profile[1]}")
        data_df = pd.read_csv(data_dir, parse_dates=["Date Time, GMT-07:00"], date_format=DATE_TIME, na_values='-1')
        data_df = data_df.dropna()
        data_df["Date Time, GMT-07:00"] = data_df["Date Time, GMT-07:00"].dt.round("h")
        if period == "increase":
            data_df = data_df[data_df["Date Time, GMT-07:00"] <= datetime.strptime('2023-06-05 23:00:00', DATE_TIME)]
        elif period == "decrease":
            data_df = data_df[data_df["Date Time, GMT-07:00"] <= datetime.strptime('2023-06-16 12:00:00', DATE_TIME)]
        df_merge = pd.merge(data_df, pressure, on="Date Time, GMT-07:00")
        r_score = plot_raw(df_merge["Date Time, GMT-07:00"], df_merge["Lake depth (m)"], df_merge["y"].astype(np.int64),
                           profile,
                           period, num_profiles)
        r_scores.append(r_score)
    r_df = pd.DataFrame({"Profiles": profiles, "R Correlation": r_scores})
    r_df.to_csv(f'plot_result/scatter/{period}/{num_profiles}/r_score.csv', index=False, na_rep='-1')


def plot_raw(date_time, lake_level, pixel_level, profile, period, num_profiles):
    fig = plt.figure(figsize=(12, 10))
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes = plt.gca()
    df = pd.DataFrame({"datetime": date_time, "x": lake_level, "y": pixel_level})
    corr = df[["x", "y"]].corr()
    r_corr = corr["y"].array[0]
    df["cat"] = pd.cut(pd.to_datetime(df.datetime).dt.hour,
                       bins=[0, 4, 8, 12, 16, 20, 24],
                       labels=['0:00 to 4:00', '4:00 to 8:00', '8:00 to 12:00', '12:00 to 16:00', '16:00 to 20:00',
                               '20:00 to 0:00'],
                       right=False,
                       include_lowest=True)
    groups = df.groupby('cat', observed=False)
    for name, group in groups:
        axes.plot(group.y, group.x, marker='o', linestyle='', ms=8, label=name)
    axes.legend(fontsize=14)
    value_text = "Pearson's r correlation = {:.6f}".format(r_corr)
    if period == "decrease":
        axes.xaxis.set_major_locator(ticker.MultipleLocator(10))
        axes.xaxis.set_minor_locator(ticker.MultipleLocator(1))
        period_text = DECREASE_PERIOD
    else:
        axes.xaxis.set_major_locator(ticker.MultipleLocator(20))
        axes.xaxis.set_minor_locator(ticker.MultipleLocator(5))
        period_text = INCREASE_PERIOD
    axes.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    axes.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

    axes.tick_params(axis='both', which='major', labelsize=14)
    axes.tick_params(axis='x', which='minor', labelsize=14)



    axes.set_xlabel("Pixelated water level (px)", fontsize=16)
    axes.set_ylabel("Water depth relative to pressure sensor (m)", fontsize=16)
    axes.set_title(f"Scatter plot of Pixelated water level vs relative water depth using segmented profile"
                   f" {profile[0]}-{profile[1]}\n"
                   f"{period_text}. "
                   f"{value_text}", fontsize=16)
    plt.savefig(f'plot_result/scatter/{period}/{num_profiles}/scatter_plot_{profile[0]}_{profile[1]}.png', bbox_inches='tight')
    plt.close(fig)
    return r_corr


if __name__ == '__main__':
    pressure_df = pd.read_csv("Lake_air_pressure.csv", parse_dates=["Date Time, GMT-07:00"], date_format=DATE_TIME)
    plot_scatter_raw(pressure_df, "decrease", 250)
    plot_scatter_raw(pressure_df, "decrease", 350)
    plot_scatter_raw(pressure_df, "increase", 250)
    plot_scatter_raw(pressure_df, "increase", 350)
