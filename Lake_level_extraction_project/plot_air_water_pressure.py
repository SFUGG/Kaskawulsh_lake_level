from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import matplotlib.transforms
import numpy as np

DATE_FORMAT = '%m/%d/%y %I:%M:%S  %p'


def plot_air_water_pres(fig_size, mark_up, save_dir):
    fig = plt.figure(figsize=fig_size)
    axes = plt.gca()
    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    axes.xaxis.set_major_locator(mdates.DayLocator())
    axes.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 4)))
    plt.plot(lake_df["Date Time, GMT-07:00"], lake_df["Abs Pres, kPa (LGR S/N: 20095431, SEN S/N: 20095431)"])
    #fig.autofmt_xdate()
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes.set_ylim([80, 230])
    axes.yaxis.set_ticks(np.arange(80, 230, 10))
    axes.yaxis.set_ticks(np.arange(80, 230, 1), minor=True)
    axes.tick_params(axis='x', which='major', labelsize=14)
    axes.tick_params(axis='y', which='major', labelsize=14)
    plt.xticks(rotation=45)
    axes.set_xlabel("Date time", fontsize=16)
    axes.set_ylabel("Absolute pressure (kPa)", fontsize=16)
    axes.set_title("Plot for Air + Water pressure from 05/30/23 10:00 AM to 06/22/23 11:30 PM on 30 minutes interval", fontsize=16)
    if mark_up:
        time_marker = ["05/31/23 02:00:00  PM", "06/05/23 11:00:00  PM", "06/12/23 11:00:00  PM"]
        time_marker = [datetime.strptime(item, DATE_FORMAT) for item in time_marker]
        value_marker = [141.882, 188.544, 215.933]
        annos_list = ["(Air+lake) pressure start recording on 05/31/23 02:00 PM at 141.882 kPa",
                  "Pressure drop from 188.544 to 183.472 kPa\n between 06/05/23 11:00 - 11:30 PM",
                  "Pressure reaches maximum on 06/12/23 11:00 PM at 215.933 kPa"]
        xy_texts = [(10, -15), (10, -50), (10, 12)]
        plt.plot(time_marker, value_marker, 'ro', markersize=2)
        for x, y, anno, xy_text in zip(time_marker, value_marker, annos_list, xy_texts):
            plt.annotate(anno, (mdates.date2num(x), y), xytext=xy_text,
                     textcoords='offset points', arrowprops=dict(arrowstyle='-|>'), fontsize=12)
    plt.savefig(save_dir, bbox_inches='tight')

def plot_air_pres(fig_size, save_dir):
    fig = plt.figure(figsize=fig_size)
    axes = plt.gca()
    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    axes.xaxis.set_major_locator(mdates.DayLocator())
    axes.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 4)))
    plt.plot(air_df["Date Time, GMT-07:00"], air_df["Abs Pres, kPa (LGR S/N: 21248883, SEN S/N: 21248883)"])
    #fig.autofmt_xdate()
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes.set_ylim([85, 100])
    axes.yaxis.set_ticks(np.arange(85, 100, 1))
    axes.yaxis.set_ticks(np.arange(85, 100, 0.2), minor=True)
    axes.tick_params(axis='x', which='major', labelsize=14)
    axes.tick_params(axis='y', which='major', labelsize=14)
    plt.xticks(rotation=45)
    axes.set_xlabel("Date time", fontsize=16)
    axes.set_ylabel("Absolute pressure (kPa)", fontsize=16)
    axes.set_title("Plot for Air pressure from 05/30/23 10:00 AM to 06/22/23 11:30 PM on 30 minutes interval", fontsize=18)
    plt.savefig(save_dir, bbox_inches='tight')

def plot_lake_pres(fig_size, mark_up, save_dir):
    fig = plt.figure(figsize=fig_size)
    axes = plt.gca()

    air_water_increase = air_water_df[
        (air_water_df["Date Time, GMT-07:00"] >= datetime.strptime("05/31/23 3:00:00  PM", DATE_FORMAT)) &
        (air_water_df["Date Time, GMT-07:00"] <= datetime.strptime("06/05/23 11:00:00  PM", DATE_FORMAT))]
    air_water_decrease = air_water_df[
        (air_water_df["Date Time, GMT-07:00"] >= datetime.strptime("06/15/23 3:00:00  PM", DATE_FORMAT)) & (
                air_water_df["Date Time, GMT-07:00"] <= datetime.strptime("06/16/23 12:00:00  PM", DATE_FORMAT))]

    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    axes.xaxis.set_major_locator(mdates.DayLocator())
    axes.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 4)))
    plt.plot(air_water_df["Date Time, GMT-07:00"], air_water_df["Lake pressure (kpa)"])
    plt.plot(air_water_increase["Date Time, GMT-07:00"], air_water_increase["Lake pressure (kpa)"], label="Increasing lake level period")
    plt.plot(air_water_decrease["Date Time, GMT-07:00"], air_water_decrease["Lake pressure (kpa)"], label="Decreasing lake level period", color='m')
    plt.legend(loc="upper left")
    #fig.autofmt_xdate()
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes.set_ylim([-10, 140])
    axes.yaxis.set_ticks(np.arange(-10, 140, 10))
    axes.yaxis.set_ticks(np.arange(-10, 140, 1), minor=True)
    axes.tick_params(axis='x', which='major', labelsize=14)
    axes.tick_params(axis='y', which='major', labelsize=14)
    plt.xticks(rotation=45)
    axes.set_xlabel("Date time", fontsize=16)
    axes.set_ylabel("Absolute pressure (kPa)", fontsize=16)
    axes.set_title("Plot for Lake pressure from 05/30/23 10:00 AM to 06/22/23 11:30 PM on 30 minutes interval", fontsize=18)
    if mark_up:
        time_marker = ["05/31/23 02:00:00  PM", "06/05/23 11:00:00  PM", "06/12/23 8:00:00  PM", "06/16/23 12:00:00  PM"]
        time_marker = [datetime.strptime(item, DATE_FORMAT) for item in time_marker]
        value_marker = [51.425, 98.072, 126.684, 0.187]
        annos_list = ["Lake pressure start recording on 05/31/23 02:00 PM at 51.425 kPa",
                    "Pressure drop from 98.072 to 92.771 kPa\n between 06/05/23 11:00 - 11:30 PM",
                    "Pressure reaches maximum on 06/12/23 8:00 PM at 126.684 kPa",
                    "Pressure reach 0 kpa on 06/16/23 12:00 PM"]
        xy_texts = [(10, -15), (10, -50), (10, 12), (5, 20)]
        plt.plot(time_marker, value_marker, 'ro', markersize=5)
        for x, y, anno, xy_text in zip(time_marker, value_marker, annos_list, xy_texts):
            plt.annotate(anno, (mdates.date2num(x), y), xytext=xy_text,
                     textcoords='offset points', arrowprops=dict(arrowstyle='-|>'), fontsize=12)
    plt.savefig(save_dir, bbox_inches='tight')


def plot_lake_depth(fig_size, mark_up, save_dir):
    fig = plt.figure(figsize=fig_size)

    air_water_increase = air_water_df[
        (air_water_df["Date Time, GMT-07:00"] >= datetime.strptime("05/31/23 3:00:00  PM", DATE_FORMAT)) &
        (air_water_df["Date Time, GMT-07:00"] <= datetime.strptime("06/05/23 11:00:00  PM", DATE_FORMAT))]
    air_water_decrease = air_water_df[
        (air_water_df["Date Time, GMT-07:00"] >= datetime.strptime("06/15/23 3:00:00  PM", DATE_FORMAT)) & (
                    air_water_df["Date Time, GMT-07:00"] <= datetime.strptime("06/16/23 12:00:00  PM", DATE_FORMAT))]

    axes = plt.gca()
    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    axes.xaxis.set_major_locator(mdates.DayLocator())
    axes.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 4)))
    plt.plot(air_water_df["Date Time, GMT-07:00"], air_water_df["Lake depth (m)"])
    plt.plot(air_water_increase["Date Time, GMT-07:00"], air_water_increase["Lake depth (m)"], label="Increasing lake level period")
    plt.plot(air_water_decrease["Date Time, GMT-07:00"], air_water_decrease["Lake depth (m)"], label="Decreasing lake level period", color='m')
    plt.legend(loc="upper left")
    #fig.autofmt_xdate()
    plt.grid(axis='both', which='major', linewidth=1)
    plt.grid(axis='both', which='minor', linewidth=0.2)
    axes.set_ylim([-1, 13])
    axes.yaxis.set_ticks(np.arange(-1, 13, 0.5))
    axes.yaxis.set_ticks(np.arange(-1, 13, 0.1), minor=True)
    axes.tick_params(axis='x', which='major', labelsize=14)
    axes.tick_params(axis='y', which='major', labelsize=14)
    plt.xticks(rotation=45)
    axes.set_xlabel("Date time", fontsize=16)
    axes.set_ylabel("Water depth relative to pressure sensor (m)", fontsize=16)
    axes.set_title("Plot for Water depth relative to pressure sensor from "
                   "05/30/23 10:00 AM to 06/22/23 11:30 PM on 30 minutes interval", fontsize=18)
    if mark_up:
        time_marker = ["05/31/23 02:00:00  PM", "06/05/23 11:00:00  PM", "06/12/23 8:00:00  PM", "06/16/23 12:00:00  PM"]
        time_marker = [datetime.strptime(item, DATE_FORMAT) for item in time_marker]
        value_marker = [5.247, 10.007, 12.927, 0.019]
        annos_list = ["Lake level start recording on 05/31/23 02:00 PM at 5.247 m",
                    "Level drop from 10.007 to 9.466 m\n between 06/05/23 11:00 - 11:30 PM",
                    "Level reaches maximum on 06/12/23 8:00 PM at 12.927 m",
                    "Level reaches 0 m on 06/16/23 12:00 PM"]
        xy_texts = [(10, -25), (10, -50), (30, -10), (5, 20)]
        plt.plot(time_marker, value_marker, 'ro', markersize=2)
        for x, y, anno, xy_text in zip(time_marker, value_marker, annos_list, xy_texts):
            plt.annotate(anno, (mdates.date2num(x), y), xytext=xy_text,
                     textcoords='offset points', arrowprops=dict(arrowstyle='-|>'), fontsize=12)
    plt.savefig(save_dir, bbox_inches='tight')

if __name__ == '__main__':
    figsize = (19, 11)
    lake_df = pd.read_csv("raw_data/20095431_LakeLevel.csv",
                          parse_dates=["Date Time, GMT-07:00"], date_format=DATE_FORMAT)
    air_df = pd.read_csv("raw_data/21248883_AirPressure.csv",
                         parse_dates=["Date Time, GMT-07:00"], date_format=DATE_FORMAT)
    air_water_df = pd.read_csv("Lake_air_pressure.csv", parse_dates=["Date Time, GMT-07:00"],
                               date_format='%Y-%m-%d %H:%M:%S')
    plot_air_water_pres(figsize, True, "plot_result/metadata/air_lake_pres_markup.png")
    plot_air_water_pres(figsize, False, "plot_result/metadata/air_lake_pres.png")
    plot_air_pres(figsize, "plot_result/metadata/air_pres.png")
    plot_lake_pres(figsize, True, "plot_result/metadata/lake_pres_markup.png")
    plot_lake_pres(figsize, False, "plot_result/metadata/lake_pres.png")
    plot_lake_depth(figsize, True, "plot_result/metadata/lake_depth_markup.png")
    plot_lake_depth(figsize, False, "plot_result/metadata/lake_depth.png")
