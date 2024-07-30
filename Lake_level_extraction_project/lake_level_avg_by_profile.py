import glob
import os
from pathlib import Path

import cv2 as cv
import pandas as pd
import numpy as np


def average_by_profile_windows(image_directory, start_profiles, end_profiles, num_profiles):
    windows = np.arange(start=start_profiles, stop=end_profiles, step=num_profiles)
    for start_window in windows:
        end_window = start_window + num_profiles
        if end_window >= end_profiles:
            end_window = end_profiles

        start_df = pd.read_csv(f'coord_by_horizontal_profile/{image_directory}/lake_level_{start_window}_profile.csv', na_values="-1")
        average_array = np.full((start_df.shape[0], num_profiles), np.nan)
        average_array[:, 0] = start_df["y"].array
        for idx, profile in enumerate(np.arange(start_window + 1, end_window), start=1):
            profile_df = pd.read_csv(f'coord_by_horizontal_profile/{image_directory}/lake_level_{profile}_profile.csv', na_values="-1")
            average_array[:, idx] = profile_df["y"].array
        average_y = np.nanmean(average_array, axis=1)
        start_df["y"] = average_y
        start_df["y"] = start_df["y"].fillna(-1).astype("int64")
        start_df.to_csv(os.path.join(f'coord_horizontal/{image_directory}/{num_profiles}', f'lake_level_{start_window}_{end_window-1}.csv'), index=False,
                        na_rep='-1')


if __name__ == '__main__':
    images_dir = "decrease"
    average_by_profile_windows(images_dir, 500, 2750, 250)
    average_by_profile_windows(images_dir, 350, 2800, 350)
    images_dir = "increase"
    average_by_profile_windows(images_dir, 0, 7392, 350)
    average_by_profile_windows(images_dir, 0, 7392, 250)
    images_dir = "2022"
    average_by_profile_windows(images_dir, 2100, 3000, 300)
    average_by_profile_windows(images_dir, 2000, 3100, 100)
    images_dir = "2022_seawall"
    average_by_profile_windows(images_dir, 3925, 4080, 155)

