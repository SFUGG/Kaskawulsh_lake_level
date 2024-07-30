from plot_scatter import YEAR_2022_PEROD

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.transforms
import cv2 as cv

DATE_TIME = '%Y-%m-%d %H:%M:%S'


def plot_displacement(displaced, date_time, title, output):
    fig = plt.figure(figsize=(16, 5))
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes = plt.gca()
    for i in range(displaced.shape[1]):
        axes.plot(date_time, displaced[0, i] - displaced[:, i], marker='.', linestyle='-', label=f"Point {i + 1}")
    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    dx = 0 / 72.
    dy = -15 / 72.
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)
    for label in axes.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)

    axes.xaxis.set_major_locator(mdates.DayLocator())
    axes.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
    axes.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 8)))

    axes.yaxis.set_major_locator(ticker.MultipleLocator(1))

    axes.tick_params(axis='both', which='major', labelsize=14)
    axes.set_ylabel("Pixel displacement (px)", fontsize=16)
    axes.set_title(title, fontsize=18)
    plt.savefig(output, bbox_inches='tight')
    plt.close(fig)


def plot_displacement_all(points_x, points_y, date_time):
    title = f"Time series plot X-Pixel displacement of tracked static points\n{YEAR_2022_PEROD}"
    output = "plot_result/displacement/x_displacement_2022.jpg"
    plot_displacement(points_x, date_time, title, output)
    title = f"Time series plot Y-Pixel displacement of tracked static points\n{YEAR_2022_PEROD}"
    output = "plot_result/displacement/y_displacement_2022.jpg"
    plot_displacement(points_y, date_time, title, output)

def mark_image(points_x, points_y, ref_image):
    point1_x = points_x[0, 0]
    point2_x = points_x[0, 1]
    point1_y = points_y[0, 0]
    point2_y = points_y[0, 1]
    image = cv.imread(ref_image, cv.IMREAD_COLOR)
    cv.circle(image, (point1_x, point1_y), 10, (0, 0, 255), -1)
    cv.circle(image, (point2_x, point2_y), 10, (0, 0, 255), -1)
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(image, f'1', (point1_x - 30, point1_y - 10), font, 5, (0, 0, 255), 5, cv.LINE_AA)
    cv.putText(image, f'2', (point2_x + 20, point2_y - 10), font, 5, (0, 0, 255), 5, cv.LINE_AA)
    cv.imwrite("plot_result/ref_static_points.jpeg", image)


if __name__ == '__main__':
    data_df = pd.read_csv("static_points_2022.csv", parse_dates=["Date Time, GMT-07:00"], date_format=DATE_TIME,
                          na_values='-1')
    X = np.asarray(data_df[["Pt 1 (x)", "Pt 2 (x)"]]).astype(np.int64)
    Y = np.asarray(data_df[["Pt 1 (y)", "Pt 2 (y)"]]).astype(np.int64)
    plot_displacement_all(X, Y, data_df["Date Time, GMT-07:00"].dt.round("h"))
    mark_image(X, Y, "Marked_photo/2022/IM_00002.png")
