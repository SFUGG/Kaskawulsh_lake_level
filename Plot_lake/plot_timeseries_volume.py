from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.transforms
from scipy.interpolate import (CubicSpline, Akima1DInterpolator,
                               PchipInterpolator, KroghInterpolator, BarycentricInterpolator)

INTERPOLATION_METHOD = {
    'piecewise': np.interp,
    'cubic_spline': CubicSpline,
    'akima': Akima1DInterpolator,
    'pchip': PchipInterpolator,
    'krogh': KroghInterpolator,
    'barycentric': BarycentricInterpolator
}
DATE_TIME = '%Y-%m-%d %H:%M:%S'
DECREASE_PERIOD = "from 2023-06-15 15:00:00 to 2023-06-16 12:00:00"
DECREASE_PERIOD_NO_CUTOFF = "from 2023-06-15 15:00:00 to 2023-06-17 05:00:00"
INCREASE_PERIOD = "from 2023-05-31 15:00:00 to 2023-06-05 23:00:00"
FULL_PERIOD = "from 2023-05-31 15:00:00 to 2023-06-16 12:00:00"
PRESSURE_SENSOR_Z_GLO = 971.571


def interpolate_data(x_interpolate, x_observed, y_observed, method='piecewise'):
    if method == 'piecewise':
        y_interpolate = INTERPOLATION_METHOD['piecewise'](x_interpolate, x_observed, y_observed)
    else:
        y_interpolate = INTERPOLATION_METHOD[method](x_observed, y_observed)(x_interpolate)
    return y_interpolate


def plot_interpolation_result(volume, elevation):
    elevation_interpolate = np.arange(elevation.min(), elevation.max() + 0.005, 0.01)
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.set_ylabel("Height above mean sea level (m)")
    ax.set_xlabel(r"Volume ($10^{3}\,m^{3}$)")

    for method in ['piecewise', 'cubic_spline', 'akima', 'pchip']:
        volume_interpolate = interpolate_data(elevation_interpolate, elevation, volume, method)
        ax.plot(volume_interpolate, elevation_interpolate, '-', label=method)

    ax.plot(volume, elevation, 'o', markersize=5)

    ax.legend()
    ax.grid()
    ax.set_title("Volume-elevation interpolation curves from Sept2018 DEM", fontsize=16)
    plt.savefig('volume_interps_sept2018', bbox_inches='tight')
    plt.close(fig)


def plot_timeseries_volume_pressure_sensor(pressure, elevation_look_up, volume_look_up):
    elevation_interpolate = np.arange(elevation_look_up.min(), elevation_look_up.max() + 0.005, 0.01).round(2)
    volume_interpolate = interpolate_data(elevation_interpolate, elevation_look_up,
                                          volume_look_up, 'cubic_spline')
    pressure = pressure[
        pressure["Date Time, GMT-07:00"] >= datetime.strptime('2023-05-31 15:00:00', DATE_TIME)]
    pressure = pressure[
        pressure["Date Time, GMT-07:00"] <= datetime.strptime('2023-06-16 12:00:00', DATE_TIME)]
    look_up = pd.DataFrame({
        "Lake depth (m)": elevation_interpolate, "Volume (m^3)": volume_interpolate
    })
    merge = pd.merge(pressure, look_up, how='left', on=['Lake depth (m)'])

    fig = plt.figure(figsize=(19, 11))
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes = plt.gca()
    axes.plot(merge['Date Time, GMT-07:00'], merge['Volume (m^3)'], linestyle='-')
    dx = 0 / 72.
    dy = -15 / 72.
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)
    for label in axes.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)

    axes.xaxis.set_major_locator(mdates.DayLocator())
    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    axes.yaxis.set_major_locator(ticker.MultipleLocator(100))
    axes.yaxis.set_minor_locator(ticker.MultipleLocator(10))

    axes.set_ylabel(r"Volume ($10^{3}\,m^{3}$)", fontsize=16)
    axes.tick_params(axis='both', which='major', labelsize=14)
    axes.set_title(f"Time series plot of lake volume using pressure sensor data\n"
                   f"{FULL_PERIOD}", fontsize=18)
    plt.savefig(f'ts_volume_pressure.jpeg',
                bbox_inches='tight')
    plt.close(fig)


def plot_timeseries_volume_georef(georef, elevation_look_up, volume_look_up, period):
    elevation_interpolate = np.arange(elevation_look_up.min(), elevation_look_up.max() + 0.005, 0.01).round(2)
    volume_interpolate = interpolate_data(elevation_interpolate, elevation_look_up,
                                          volume_look_up, 'cubic_spline')
    look_up = pd.DataFrame({
        "z": elevation_interpolate, "Volume (m^3)": volume_interpolate
    })
    merge = pd.merge(georef, look_up, how='left', on=['z'])
    fig = plt.figure(figsize=(12, 10))
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes = plt.gca()
    axes.plot(merge['Date Time, GMT-07:00'], merge['Volume (m^3)'], marker='.', linestyle='-')
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
        axes.yaxis.set_major_locator(ticker.MultipleLocator(100))
        axes.yaxis.set_minor_locator(ticker.MultipleLocator(10))
        period_text = DECREASE_PERIOD
    elif period == 'increase':
        axes.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 4)))
        axes.yaxis.set_major_locator(ticker.MultipleLocator(100))
        axes.yaxis.set_minor_locator(ticker.MultipleLocator(10))
        period_text = INCREASE_PERIOD

    axes.tick_params(axis='x', which='minor', labelsize=14)
    axes.tick_params(axis='both', which='major', labelsize=14)
    axes.set_ylabel(r"Volume ($10^{3}\,m^{3}$)", fontsize=16)
    axes.set_title(f"Time series plot of lake volume using georeferenced\n"
                   f"{period_text}", fontsize=18)
    plt.savefig(f'ts_volume_georef_{period}.jpeg',
                bbox_inches='tight')
    plt.close(fig)

def plot_timeseries_volume_combine(pressure, georef, elevation_look_up, volume_look_up, period):
    elevation_interpolate = np.arange(elevation_look_up.min(), elevation_look_up.max() + 0.005, 0.01).round(2)
    volume_interpolate = interpolate_data(elevation_interpolate, elevation_look_up,
                                          volume_look_up, 'cubic_spline')
    look_up = pd.DataFrame({
        "z": elevation_interpolate, "Volume (m^3)": volume_interpolate
    })
    merge_georef = pd.merge(georef, look_up, how='left', on=['z'])

    if period == 'increase':
        pressure = pressure[
                    pressure["Date Time, GMT-07:00"] >= datetime.strptime('2023-05-31 15:00:00', DATE_TIME)]
        pressure = pressure[
                    pressure["Date Time, GMT-07:00"] <= datetime.strptime('2023-06-05 23:00:00', DATE_TIME)]
    elif period == 'decrease':
        pressure = pressure[
            pressure["Date Time, GMT-07:00"] >= datetime.strptime('2023-06-15 15:00:00', DATE_TIME)]
        pressure = pressure[
            pressure["Date Time, GMT-07:00"] <= datetime.strptime('2023-06-16 12:00:00', DATE_TIME)]
    look_up.rename(columns={'z': 'Lake depth (m)'}, inplace=True)
    merge_pressure = pd.merge(pressure, look_up, how='left', on=['Lake depth (m)'])

    fig = plt.figure(figsize=(12, 10))
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes = plt.gca()
    axes.plot(merge_georef['Date Time, GMT-07:00'], merge_georef['Volume (m^3)'], marker='.', linestyle='-',
              label='Georeferenced data')
    axes.plot(merge_pressure['Date Time, GMT-07:00'], merge_pressure['Volume (m^3)'], marker='.', linestyle='-',
              label='Pressure sensor data')
    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
    dx = 0 / 72.
    dy = -15 / 72.
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)
    for label in axes.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)

    axes.legend(fontsize=14)
    axes.xaxis.set_major_locator(mdates.DayLocator())
    axes.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
    if period == 'decrease':
        axes.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 2)))
        axes.yaxis.set_major_locator(ticker.MultipleLocator(100))
        axes.yaxis.set_minor_locator(ticker.MultipleLocator(10))
        period_text = DECREASE_PERIOD
    elif period == 'increase':
        axes.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 4)))
        axes.yaxis.set_major_locator(ticker.MultipleLocator(100))
        axes.yaxis.set_minor_locator(ticker.MultipleLocator(10))
        period_text = INCREASE_PERIOD

    axes.tick_params(axis='x', which='minor', labelsize=14)
    axes.tick_params(axis='both', which='major', labelsize=14)
    axes.set_ylabel(r"Volume ($10^{3}\,m^{3}$)", fontsize=16)
    axes.set_title(f"Time series plot of lake volume using georeferenced and pressure sensor data\n"
                   f"{period_text}", fontsize=18)
    plt.savefig(f'ts_volume_combine_{period}.jpeg',
                bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    hypersometric_df = pd.read_csv('data/hypsometric_curve_area.csv')
    plot_interpolation_result(hypersometric_df['volumes (m^3)'].to_numpy(),
                              hypersometric_df['elevation (m)'].to_numpy())
    pressure_df = pd.read_csv('data/Lake_air_pressure.csv',
                              parse_dates=["Date Time, GMT-07:00"], date_format=DATE_TIME, na_values='-1')
    pressure_df['Lake depth (m)'] = np.round(pressure_df['Lake depth (m)'] + PRESSURE_SENSOR_Z_GLO, 2)
    pressure_df["Date Time, GMT-07:00"] = pressure_df["Date Time, GMT-07:00"].dt.round("h")

    plot_timeseries_volume_pressure_sensor(pressure_df,
                                           hypersometric_df['elevation (m)'].to_numpy(),
                                           hypersometric_df['volumes (m^3)'].to_numpy())
    decrease_df = pd.read_csv('data/elevation_result_decrease_glo.csv',
                              parse_dates=["Date Time, GMT-07:00"], date_format=DATE_TIME, na_values='-1').dropna()
    decrease_df['z'] = decrease_df['z'].round(2)
    decrease_df["Date Time, GMT-07:00"] = decrease_df["Date Time, GMT-07:00"].dt.round("h")
    plot_timeseries_volume_georef(decrease_df, hypersometric_df['elevation (m)'].to_numpy(),
                                  hypersometric_df['volumes (m^3)'].to_numpy(), 'decrease')
    increase_df = pd.read_csv('data/elevation_result_increase_glo.csv',
                              parse_dates=["Date Time, GMT-07:00"], date_format=DATE_TIME, na_values='-1').dropna()
    increase_df['z'] = increase_df['z'].round(2)
    increase_df["Date Time, GMT-07:00"] = increase_df["Date Time, GMT-07:00"].dt.round("h")
    plot_timeseries_volume_georef(increase_df, hypersometric_df['elevation (m)'].to_numpy(),
                                  hypersometric_df['volumes (m^3)'].to_numpy(), 'increase')
    plot_timeseries_volume_combine(pressure_df, increase_df, hypersometric_df['elevation (m)'].to_numpy(),
                                  hypersometric_df['volumes (m^3)'].to_numpy(), 'increase')
    plot_timeseries_volume_combine(pressure_df, decrease_df, hypersometric_df['elevation (m)'].to_numpy(),
                                  hypersometric_df['volumes (m^3)'].to_numpy(), 'decrease')
