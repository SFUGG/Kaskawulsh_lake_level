import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker
import cv2 as cv

from plot_scatter import DECREASE_PERIOD, YEAR_2022_PEROD


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
    if period == 'decrease':
        axes.yaxis.set_major_locator(ticker.MultipleLocator(5))
        axes.yaxis.set_minor_locator(ticker.MultipleLocator(1))
        period_text = DECREASE_PERIOD
    elif period == '2022':
        axes.yaxis.set_major_locator(ticker.MultipleLocator(50))
        axes.yaxis.set_minor_locator(ticker.MultipleLocator(10))
        period_text = YEAR_2022_PEROD

    axes2.set_ylabel("Vertical pixel")
    axes.set_ylabel("Number of pixelated lake level")
    axes.set_xlabel("Horizontal Profile")
    axes.set_title(f"Plot of Number of pixelated lake level used by Horizontal Profile "
                   f"{period_text}")
    plt.savefig(f"plot_result/histogram_{period}_{num_profiles}.png", bbox_inches='tight')


if __name__ == '__main__':
    dir_folder = "coord_by_horizontal_profile"
    plot_data_used_histogram(dir_folder, "IM_00385.png", "decrease", 350, 7392)
    plot_data_used_histogram(dir_folder, "IM_00385.png", "decrease", 250, 7392)
    plot_data_used_histogram(dir_folder, "IM_00002.png", "2022", 300, 5888)
    plot_data_used_histogram(dir_folder, "IM_00002.png", "2022", 100, 5888)
