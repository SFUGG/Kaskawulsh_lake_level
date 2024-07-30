from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from plot_compare_prototype import poly_fit

DATE_TIME = '%Y-%m-%d %H:%M:%S'


def plot_compare(num, segment):
    decrease = pd.read_csv(f"coord_horizontal/decrease/{num}/lake_level_{segment}.csv",
                           parse_dates=["Date Time, GMT-07:00"],
                           date_format=DATE_TIME, na_values='-1')
    decrease.dropna(inplace=True)
    decrease = decrease[decrease["Date Time, GMT-07:00"] <= datetime.strptime('2023-06-16 12:00:00', DATE_TIME)]
    increase = pd.read_csv(f"coord_horizontal/increase/{num}/lake_level_{segment}.csv",
                           parse_dates=["Date Time, GMT-07:00"],
                           date_format=DATE_TIME, na_values='-1')
    increase.dropna(inplace=True)
    pressure_df = pd.read_csv("Lake_air_pressure.csv", parse_dates=["Date Time, GMT-07:00"], date_format=DATE_TIME)
    decrease["Date Time, GMT-07:00"] = decrease["Date Time, GMT-07:00"].dt.round("h")
    increase["Date Time, GMT-07:00"] = increase["Date Time, GMT-07:00"].dt.round("h")
    dec_merge = pd.merge(decrease, pressure_df, on="Date Time, GMT-07:00")
    upper_dec = dec_merge[dec_merge['Lake depth (m)'] > 5]
    lower_dec = dec_merge[dec_merge['Lake depth (m)'] <= 5]
    inc_merge = pd.merge(increase, pressure_df, on="Date Time, GMT-07:00")
    fig, ax1 = plt.subplots(figsize=(12, 10))
    ax1.grid(axis='both', which='major', linewidth=1)
    ax1.grid(axis='both', which='minor', linewidth=0.2)
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(20))
    ax1.xaxis.set_minor_locator(ticker.MultipleLocator(2))
    ax1.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

    # dec_x = dec_merge['Lake depth (m)']
    # dec_y = dec_merge['y']
    # inc_x = inc_merge['Lake depth (m)']
    # inc_y = inc_merge['y']
    upper_dec_x = upper_dec['y']
    upper_dec_y = upper_dec['Lake depth (m)']
    dec_x = dec_merge['y']
    dec_y = dec_merge['Lake depth (m)']
    lower_dec_x = lower_dec['y']
    lower_dec_y = lower_dec['Lake depth (m)']
    inc_x = inc_merge['y']
    inc_y = inc_merge['Lake depth (m)']
    upper_dec_x_int = np.arange(upper_dec_x.min(), upper_dec_x.max(), 0.1)
    lower_dec_x_int = np.arange(lower_dec_x.min(), lower_dec_x.max(), 0.1)
    inc_x_int = np.arange(inc_x.min(), inc_x.max(), 0.1)
    lower_dec_p, lower_dec_y_int, lower_dec_r2 = poly_fit(lower_dec_x_int, lower_dec_x, lower_dec_y)
    upper_dec_p, upper_dec_y_int, upper_dec_r2 = poly_fit(upper_dec_x_int, upper_dec_x, upper_dec_y)
    inc_p, inc_y_int, inc_r2 = poly_fit(inc_x_int, inc_x, inc_y)
    ax1.scatter(upper_dec_x, upper_dec_y, color='tab:blue', label='Decreasing period 06/15 16:00 to 06/16 00:00')

    ax1.plot(upper_dec_x_int, upper_dec_y_int,
             label=f'Transform function: y = {upper_dec_p[0]:.6f} * x + {upper_dec_p[1]:.6f}\nr2 error = {upper_dec_r2:.6f}', color='y')
    ax1.scatter(lower_dec_x, lower_dec_y, color='tab:red', label='Decreasing period 06/16 00:00 to 06/16 12:00')
    ax1.plot(lower_dec_x_int, lower_dec_y_int,
             label=f'Transform function: y = {lower_dec_p[0]:.6f} * x + {lower_dec_p[1]:.6f}\nr2 error = {lower_dec_r2:.6f}',
             color='m')
    ax1.scatter(inc_x, inc_y, color='tab:orange', label='Increasing period 06/01 14:00 to 06/04 09:00')
    ax1.plot(inc_x_int, inc_y_int,
             label=f'Transform function: y = {inc_p[0]:.6f} * x + {inc_p[1]:.6f}\nr2 error = {inc_r2:.6f}', color='c')
    ax1.tick_params(axis='both', which='major', labelsize=14)
    ax1.tick_params(axis='x', which='minor', labelsize=14)
    ax1.legend(fontsize=14)
    ax1.set_ylabel("Water depth relative to pressure sensor (m)", fontsize=16)
    ax1.set_xlabel("Pixelated water level (px)", fontsize=16)
    ax1.set_title(
        f"Scatter plot of Pixelated water level vs water depth relative to pressure sensor using segmented\n profile"
        f" {segment} between increasing and decreasing periods (with split decreasing)", fontsize=18)
    plt.savefig(f"plot_result/transform/compare_scatter_split/{num}/compare_scatter_split_{segment}.png",
                bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    m = 250
    windows = np.arange(start=500, stop=2749, step=m)
    for start_window in windows:
        end_window = start_window + m - 1
        if end_window >= 2749:
            end_window = 2749
        plot_compare(m, f'{start_window}_{end_window}')

    m = 350
    windows = np.arange(start=350, stop=2799, step=m)
    for start_window in windows:
        end_window = start_window + m - 1
        if end_window >= 2799:
            end_window = 2799
        plot_compare(m, f'{start_window}_{end_window}')
