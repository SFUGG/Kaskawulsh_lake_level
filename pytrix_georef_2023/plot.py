from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.transforms
import glob
from waterline_orthorectification import CGP_OPTIMIZATION_SCHEME, DEM_USED, OPTIMIZATION_SCHEME

DATE_TIME = '%Y-%m-%d %H:%M:%S'
PRESSURE_SENSOR_Z_GLO = 971.571
PRESSURE_SENSOR_Z_ARCTIC = 968.607

def plot_time_series(date_time, elevation, output):
    fig = plt.figure(figsize=(12, 10))
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes = plt.gca()
    axes.plot(date_time, elevation, marker='.', linestyle='-')
    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))

    dx = 0 / 72.
    dy = -15 / 72.
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)
    for label in axes.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)

    axes.xaxis.set_major_locator(mdates.DayLocator())
    axes.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
    axes.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 4)))

    axes.tick_params(axis='both', which='major', labelsize=14)
    axes.tick_params(axis='x', which='minor', labelsize=14)
    axes.set_ylabel("Elevation (m a.s.l.)", fontsize=16)
    axes.set_title(f"Time series plot of Elevation georeferenced using {dem_name}\n"
                   f"from {timeline}", fontsize=18)
    plt.savefig(f'{output}', bbox_inches='tight')


def plot_scatter(date_time, lake_level, elevation, output):
    if dem_used == 'glo':
        lake_level = lake_level + PRESSURE_SENSOR_Z_GLO
    elif dem_used == 'arctic':
        lake_level = lake_level + PRESSURE_SENSOR_Z_ARCTIC
    fig = plt.figure(figsize=(12, 10))
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes = plt.gca()
    df = pd.DataFrame({"datetime": date_time, "x": lake_level, "y": elevation})
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
    axes.yaxis.set_major_locator(ticker.MultipleLocator(1.0))
    axes.yaxis.set_minor_locator(ticker.MultipleLocator(0.2))
    axes.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
    axes.xaxis.set_minor_locator(ticker.MultipleLocator(0.2))

    axes.tick_params(axis='both', which='major', labelsize=14)
    axes.tick_params(axis='x', which='minor', labelsize=14)

    axes.set_xlabel("Elevation (m a.s.l.)", fontsize=16)
    axes.set_ylabel("Water depth measured by pressure sensor \ntranslated by water sensor elevatiom (m a.s.l)", fontsize=16)
    axes.set_title(f"Scatter plot of Elevation georeferenced using {dem_name} vs relative water depth\n"
                   f"from {timeline}\n"
                   f"{value_text}", fontsize=16)
    plt.savefig(f'{output}', bbox_inches='tight')
    plt.close(fig)

def scatter_compare(inc_z, inc_depth, dec_z, dec_depth, output):
    if dem_used == 'glo':
        inc_depth = inc_depth + PRESSURE_SENSOR_Z_GLO
        dec_depth = dec_depth + PRESSURE_SENSOR_Z_GLO
    elif dem_used == 'arctic':
        inc_depth = inc_depth + PRESSURE_SENSOR_Z_ARCTIC
        dec_depth = dec_depth + PRESSURE_SENSOR_Z_ARCTIC
    fig = plt.figure(figsize=(12, 10))
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes = plt.gca()
    axes.scatter(dec_z, dec_depth, color='tab:blue', label='Decreasing period 06/15 16:00 to 06/16 12:00')
    axes.scatter(inc_z, inc_depth, color='tab:orange', label='Increasing period 05/31 15:00 to 06/05 23:00')
    axes.tick_params(axis='both', which='major', labelsize=14)
    axes.tick_params(axis='x', which='minor', labelsize=14)
    axes.legend(fontsize=14)
    axes.set_xlabel("Elevation (m a.s.l.)", fontsize=16)
    axes.set_ylabel("Water depth measured by pressure sensor \ntranslated by water sensor elevation (m a.s.l)", fontsize=16)
    axes.set_title(f"Scatter plot of Elevation georeferenced using {dem_name} vs relative water depth\n"
                   f"from decreasing and offset increase periods", fontsize=16)
    plt.savefig(f'{output}', bbox_inches='tight')


increase = 0

opt = 'opt8'
optimization_scheme = OPTIMIZATION_SCHEME[opt]

dem_used = DEM_USED[0]

if dem_used == 'glo':
    dem_name = "2018Sep DEM"
else:
    dem_name = "ArcticDEM"

input_prefix = optimization_scheme["prefix"]
output_prefix = optimization_scheme['output']

elevation_inc = f"csv_data/elevation_result_increase_{dem_used}{input_prefix}.csv"
elevation_dec = f"csv_data/elevation_result_decrease_{dem_used}{input_prefix}.csv"

if increase == 1:
    pressure_df = pd.read_csv("csv_data/Lake_air_pressure.csv", parse_dates=["Date Time, GMT-07:00"])
    elevation_df = pd.read_csv(elevation_inc, na_values=-1,
                               parse_dates=["Date Time, GMT-07:00"])
    elevation_df.dropna(inplace=True)
    timeline = "2023-05-31 15:00:00 to 2023-06-05 23:00:00"
    elevation_df["Date Time, GMT-07:00"] = elevation_df["Date Time, GMT-07:00"].dt.round("H")
    elevation_df = elevation_df[
        elevation_df["Date Time, GMT-07:00"] <= datetime.strptime('2023-06-05 23:00:00', DATE_TIME)]
    df_merge = pd.merge(elevation_df, pressure_df, on="Date Time, GMT-07:00")
    plot_time_series(df_merge["Date Time, GMT-07:00"], df_merge['z'],
                     f'result/ts_increase_{dem_used}{output_prefix}.png')
    plot_scatter(df_merge["Date Time, GMT-07:00"], df_merge["Lake depth (m)"], df_merge['z'],
                 f'result/scatter_increase_{dem_used}_shifted{output_prefix}')
elif increase == 0:
    pressure_df = pd.read_csv("csv_data/Lake_air_pressure.csv", parse_dates=["Date Time, GMT-07:00"])
    elevation_df = pd.read_csv(elevation_dec, na_values=-1,
                               parse_dates=["Date Time, GMT-07:00"])
    elevation_df.dropna(inplace=True)
    timeline = "from 2023-06-15 15:00:00 to 2023-06-16 12:00:00"
    elevation_df["Date Time, GMT-07:00"] = elevation_df["Date Time, GMT-07:00"].dt.round("H")

    df_merge = pd.merge(elevation_df, pressure_df, on="Date Time, GMT-07:00")
    plot_time_series(df_merge["Date Time, GMT-07:00"], df_merge['z'],
                     f'result/ts_decrease_{dem_used}{output_prefix}.png')

    df_merge = df_merge[
        df_merge["Date Time, GMT-07:00"] <= datetime.strptime('2023-06-16 12:00:00', DATE_TIME)]

    plot_scatter(df_merge["Date Time, GMT-07:00"], df_merge["Lake depth (m)"], df_merge['z'],
                 f'result/scatter_decrease_{dem_used}_shifted{output_prefix}')

compare = 0

if compare == 1:
    pressure_df = pd.read_csv("csv_data/Lake_air_pressure.csv", parse_dates=["Date Time, GMT-07:00"])
    inc_elevation_df = pd.read_csv(elevation_inc, na_values=-1,
                               parse_dates=["Date Time, GMT-07:00"])
    inc_elevation_df.dropna(inplace=True)
    inc_elevation_df["Date Time, GMT-07:00"] = inc_elevation_df["Date Time, GMT-07:00"].dt.round("H")
    inc_elevation_df = inc_elevation_df[
        inc_elevation_df["Date Time, GMT-07:00"] <= datetime.strptime('2023-06-05 23:00:00', DATE_TIME)]
    inc_merge = pd.merge(inc_elevation_df, pressure_df, on="Date Time, GMT-07:00")

    dec_elevation_df = pd.read_csv(elevation_dec, na_values=-1,
                               parse_dates=["Date Time, GMT-07:00"])
    dec_elevation_df.dropna(inplace=True)
    dec_elevation_df["Date Time, GMT-07:00"] = dec_elevation_df["Date Time, GMT-07:00"].dt.round("H")
    dec_elevation_df = dec_elevation_df[
        dec_elevation_df["Date Time, GMT-07:00"] <= datetime.strptime('2023-06-16 12:00:00', DATE_TIME)]
    dec_merge = pd.merge(dec_elevation_df, pressure_df, on="Date Time, GMT-07:00")
    scatter_compare(inc_z=inc_merge['z'], inc_depth=inc_merge['Lake depth (m)'],
                    dec_z=dec_merge['z'], dec_depth=dec_merge['Lake depth (m)'],
                    output=f'result/scatter_compare_{dem_used}{input_prefix}')