import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from sklearn.metrics import r2_score

DATE_TIME = '%Y-%m-%d %H:%M:%S'

def poly_fit(x_int, x, y, deg=1):
    p = np.polyfit(x, y, deg)
    model = np.poly1d(p)
    r2 = r2_score(y, model(x))
    y_int = np.polyval(p, x_int)
    return p, y_int, r2

if __name__ == '__main__':
    dec_df = pd.read_csv("raw_data/compare/decrease_1500_1749.csv", parse_dates=["Date Time, GMT-07:00"], date_format=DATE_TIME, na_values='-1').dropna()
    inc_df = pd.read_csv("raw_data/compare/increase_1500_1749.csv", parse_dates=["Date Time, GMT-07:00"],
                         date_format=DATE_TIME, na_values='-1').dropna()
    lake_df = pd.read_csv("Lake_air_pressure.csv", parse_dates=["Date Time, GMT-07:00"], date_format=DATE_TIME)
    dec_df["Date Time, GMT-07:00"] = dec_df["Date Time, GMT-07:00"].dt.round("h")
    dec_merge = pd.merge(dec_df, lake_df, on="Date Time, GMT-07:00")

    inc_df["Date Time, GMT-07:00"] = inc_df["Date Time, GMT-07:00"].dt.round("h")
    inc_merge = pd.merge(inc_df, lake_df, on="Date Time, GMT-07:00")

    fig, ax1 = plt.subplots(figsize=(12, 10))
    ax1.grid(axis='both', which='major', linewidth=1)
    ax1.grid(axis='both', which='minor', linewidth=0.2)

    ax1.scatter(dec_merge['y'], dec_merge['Lake depth (m)'], label='Decreasing Period 06/15 16:00 to 06/16 12:00')
    ax1.scatter(inc_merge['y'], inc_merge['Lake depth (m)'], label='Increasing Period 06/1 14:00 to 06/04 09:00')

    ax1.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax1.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax1.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    ax1.set_xlabel("Pixelated lake-level (px)", fontsize=16)
    ax1.set_ylabel("water depth relative to pressure sensor (m)", fontsize=16)
    plt.legend(fontsize=14)
    ax1.set_title(f"Scatter and Pixelated water level vs relative water level using segmented profile"
                   f"\n{1500}-{1749} between increase and decrease period in relative water level range 6-8.5m", fontsize=18)
    plt.savefig(f'plot_result/transform/compare_prototype.png', bbox_inches='tight')
