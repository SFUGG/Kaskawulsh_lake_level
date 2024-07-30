from pathlib import Path
import re

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import cv2 as cv


DATE_TIME = '%Y-%m-%d %H:%M:%S'

PAIR = {
    1: ['IM_00394', 'IM_00054'],
    2: ['IM_00393', 'IM_00067'],
    3: ['IM_00392', 'IM_00074'],
    4: ['IM_00391', 'IM_00082'],
    5: ['IM_00389', 'IM_00096'],
    6: ['IM_00385', 'IM_00122']}


def plot_offset(pair, track):
    df_dec = pd.read_csv(f'raw_data/offset_data/raw/{pair[0]}.csv', na_values='-1')
    df_inc = pd.read_csv(f'raw_data/offset_data/raw/{pair[1]}.csv', na_values='-1')
    info_dec = track[track['image_name'] == pair[0]].reset_index()
    info_inc = track[track['image_name'] == pair[1]].reset_index()
    offset = df_inc.y - df_dec.y

    fig, ax1 = plt.subplots(figsize=(12, 8))
    ax1.grid(axis='both', which='major', linewidth=1)
    ax1.grid(axis='both', which='minor', linewidth=0.2)

    ax1.xaxis.set_major_locator(ticker.MultipleLocator(250))
    ax1.xaxis.set_minor_locator(ticker.MultipleLocator(50))
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax1.yaxis.set_minor_locator(ticker.MultipleLocator(1))

    ax1.plot(df_dec.x, offset, linestyle='-')
    ax1.set_ylabel("Pixelated water-level", fontsize=18)
    ax1.set_xlabel("Horizontal profile", fontsize=18)
    ax1.tick_params(axis='y', which='major', labelsize=14)
    ax1.tick_params(axis='x', which='major', labelsize=14, labelrotation=45)

    inc_day = info_inc.loc[0, 'Datetime']
    inc_depth = info_inc.loc[0, 'depth']
    dec_day = info_dec.loc[0, 'Datetime']
    dec_depth = info_dec.loc[0, 'depth']
    ax1.set_title(f'Offset of Pixelated water level between day {inc_day} at depth {inc_depth} m and\n'
                  f'day {dec_day} at depth {dec_depth} m', fontsize=20)
    plt.savefig(f"plot_result/offset/offset_{pair[0]}_{pair[1]}.png", bbox_inches='tight')


    #img = cv.imread(f"raw_data/offset_data/pic/{pair[1]}.JPG")
    fig, ax1 = plt.subplots(figsize=(16, 9))
    ax1.grid(axis='both', which='major', linewidth=1)
    ax1.grid(axis='both', which='minor', linewidth=0.2)

    ax1.xaxis.set_major_locator(ticker.MultipleLocator(250))
    ax1.xaxis.set_minor_locator(ticker.MultipleLocator(50))
    # ax1.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax1.yaxis.set_minor_locator(ticker.MultipleLocator(10))
    ax1.set_xlim([0, 7392])
    ax1.plot(df_dec.x, df_dec.y, linestyle='-', label='Decreasing period')
    ax1.plot(df_inc.x, df_inc.y, linestyle='-', label='Increasing period')
    plt.legend(fontsize=16)
    ax1.set_ylabel("Pixelated water-level", fontsize=18)
    ax1.set_xlabel("Horizontal profile", fontsize=18)
    ax1.tick_params(axis='y', which='major', labelsize=14)
    ax1.tick_params(axis='x', which='major', labelsize=14, labelrotation=45)
    ax1.set_title(
        f'Comparison of Pixelated water level between day {inc_day} at depth {inc_depth} m and\n'
        f'day {dec_day} at depth {dec_depth} m', fontsize=20)
    plt.savefig(f"plot_result/offset/comp_{pair[0]}_{pair[1]}.png", bbox_inches='tight')


if __name__ == '__main__':
    df_track = pd.read_csv('raw_data/offset_data/track_same_level.csv',
                           parse_dates=["Datetime"], date_format=DATE_TIME)
    for i in range(1, 7):
        pairs = PAIR[i]
        plot_offset(pairs, df_track)