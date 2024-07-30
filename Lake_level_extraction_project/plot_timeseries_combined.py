import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.transforms

DATE_TIME = '%Y-%m-%d %H:%M:%S'


def plot_timeseries_combine(displaced, sea_wall, lake, date_time):
    fig = plt.figure(figsize=(16, 10))
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes = plt.gca()
    axes.plot(date_time, lake, marker='.', linestyle='-', label="Pixelated lake level")
    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

    dx = 0 / 72.
    dy = -15 / 72.
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)
    for label in axes.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)

    axes.xaxis.set_major_locator(mdates.DayLocator())
    axes.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
    axes.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 8)))

    axes.yaxis.set_major_locator(ticker.MultipleLocator(50))
    axes.yaxis.set_minor_locator(ticker.MultipleLocator(5))

    axes2 = axes.twinx()
    axes2.yaxis.set_major_locator(ticker.MultipleLocator(5))
    axes2.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    axes2.plot(date_time, sea_wall, marker='.', color='tab:orange', linestyle='-', label="Seawall Y-pixel displacement")
    color = ['r', 'g']
    for i in range(displaced.shape[1]):
        axes2.plot(date_time, displaced[0, i] - displaced[:, i], color=color[i], marker='.', linestyle='-',
                   label=f"Static point {i + 1} Y-pixel displacement")

    axes.tick_params(axis='both', which='major', labelsize=14)
    axes2.tick_params(axis='y', which='major', labelsize=14)
    axes.set_ylabel("Pixel (px)", fontsize=16)
    axes2.set_ylabel("Pixel displacement (px)", fontsize=16)

    lines, labels = axes.get_legend_handles_labels()
    lines2, labels2 = axes2.get_legend_handles_labels()
    axes2.legend(lines + lines2, labels + labels2, fontsize=12, loc=9)
    axes.set_title(f"Time series plot of Pixelated lake level and static points and seawall displacement\n"
                   f"from 2022-07-23 04:00:00 to 2022-08-11 03:00:00", fontsize=18)
    plt.savefig("plot_result/time_series/2022/ts_combined.jpeg")


if __name__ == '__main__':
    static = pd.read_csv("static_points_2022.csv", parse_dates=["Date Time, GMT-07:00"],
                         date_format=DATE_TIME, na_values='-1')
    seawall = pd.read_csv("coord_horizontal/2022_seawall/155/lake_level_3925_4079.csv",
                          parse_dates=["Date Time, GMT-07:00"], date_format=DATE_TIME, na_values='-1')
    data = pd.read_csv("coord_horizontal/2022/100/lake_level_2900_2999.csv",
                          parse_dates=["Date Time, GMT-07:00"], date_format=DATE_TIME, na_values='-1')
    Y = np.asarray(static[["Pt 1 (y)", "Pt 2 (y)"]]).astype(np.int64)
    plot_timeseries_combine(Y, seawall['y'] - seawall['y'][0], data['y'],
                            data["Date Time, GMT-07:00"].dt.round("h"))
