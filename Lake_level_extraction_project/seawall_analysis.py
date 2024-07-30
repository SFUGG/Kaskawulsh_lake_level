import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.transforms
import cv2 as cv

DATE_TIME = '%Y-%m-%d %H:%M:%S'


def plot_data_used_histogram(csv_dir, ref_image, period, num_profiles, image_width):
    x = np.arange(start=0, stop=image_width)
    y = np.empty(image_width)
    max_num = 0
    for i in x:
        df = pd.read_csv(f"{csv_dir}/{period}/lake_level_{i}_profile.csv", na_values="-1")
        if i == 0:
            max_num = df["Date Time, GMT-07:00"].count()
        y[i] = df["y"].count()
    img = cv.imread(f"Marked_photo/{period}/{ref_image}")
    fig = plt.figure(figsize=(16, 9))
    plt.grid(axis='both', which='major', linewidth=1, zorder=2)
    plt.grid(axis='both', which='minor', linewidth=0.2, zorder=2)
    axes = plt.gca()

    axes2 = axes.twinx()
    axes2.imshow(img, interpolation='nearest', alpha=0.3, zorder=1)
    axes.plot(x, y, alpha=1)
    axes.plot([0, image_width], [max_num, max_num], label="maximum number of data possible", alpha=1)
    axes.set_xlim([0, image_width])
    axes.legend()
    axes.xaxis.set_major_locator(ticker.MultipleLocator(num_profiles))
    axes.xaxis.set_minor_locator(ticker.MultipleLocator(50))
    axes.yaxis.set_major_locator(ticker.MultipleLocator(50))
    axes.yaxis.set_minor_locator(ticker.MultipleLocator(10))

    axes2.set_ylabel("Vertical pixel")
    axes.set_ylabel("Number of pixelated level")
    axes.set_xlabel("Horizontal Profile")
    axes.set_title(f"Plot of Number of pixel level of icewall used by Horizontal Profile "
                   f"from 2022-07-23 04:00:00 to 2022-08-11 03:00:00")
    plt.savefig(f"plot_result/histogram_icewall_{num_profiles}.png", bbox_inches='tight')


def plot_seawall(date_time, pixel_level, period):
    fig = plt.figure(figsize=(16, 10))
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes = plt.gca()
    axes.plot(date_time, pixel_level, marker='.', linestyle='-')
    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

    dx = 0 / 72.
    dy = -15 / 72.
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)
    for label in axes.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)

    axes.xaxis.set_major_locator(mdates.DayLocator())
    axes.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
    axes.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 8)))
    axes.yaxis.set_major_locator(ticker.MultipleLocator(10))
    axes.yaxis.set_minor_locator(ticker.MultipleLocator(1))

    axes.tick_params(axis='both', which='major', labelsize=14)
    axes.set_ylabel("Pixel displacement (px)", fontsize=16)
    axes.set_title(f"Time series plot of icewall Pixel displacement "
                   f"from 2022-07-23 04:00:00 to 2022-08-11 03:00:00", fontsize=18)
    plt.savefig(f'plot_result/time_series/{period}/tsplot_icewall.png',
                bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    dir_folder = "coord_by_horizontal_profile"
    plot_data_used_histogram(dir_folder, "IM_00002.png", "2022_seawall", 500, 5888)
    data_df = pd.read_csv("coord_horizontal/2022_seawall/155/lake_level_3925_4079.csv",
                     parse_dates=["Date Time, GMT-07:00"], date_format=DATE_TIME, na_values='-1')
    plot_seawall(data_df["Date Time, GMT-07:00"].dt.round("h"), data_df['y'] - data_df['y'][0], '2022_seawall')