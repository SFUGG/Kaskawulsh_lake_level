import glob
import os
from pathlib import Path

import cv2 as cv
import pandas as pd
import numpy as np


def retrive_file_name(file_dir):
    return Path(file_dir).stem


vf = np.vectorize(retrive_file_name)


def extract_coord_by_image(images_director, id_color):
    images_location = glob.glob(os.path.join(f'Marked_photo/{images_director}', "*.png"))
    for image_location in images_location:
        image_name = retrive_file_name(image_location)
        image = cv.imread(image_location, cv.IMREAD_COLOR)
        image = cv.flip(image, 0)
        marked_pos = np.where(np.all(image == id_color, axis=-1))
        h, w, c = image.shape
        dummy_df = pd.DataFrame({'x': np.arange(w)})

        coord_df = pd.DataFrame({'y': marked_pos[0], 'x': marked_pos[1]})
        if np.unique(marked_pos[1]).size != marked_pos[1].size:
            coord_df = coord_df.groupby(['x']).aggregate("median")
        final_df = pd.merge(dummy_df, coord_df, how="left", on="x").fillna(-1).astype('int64')
        final_df.to_csv(os.path.join(f"coord_by_photo/{images_director}", f'{image_name}.csv'), index=False,
                        na_rep='-1')


def create_coord_by_horizontal_profiles(images_director, images_info, image_width):
    csv_locs = glob.glob(f"coord_by_photo/{images_director}/*.csv")
    files_name = vf(np.array(csv_locs))
    used_images_info = pd.merge(pd.DataFrame({"Image name": files_name}), images_info, how="inner", on="Image name")
    dummy_df = pd.DataFrame({'x': np.arange(image_width)})

    for csv_loc in csv_locs:
        image_name = retrive_file_name(csv_loc)
        df = pd.read_csv(csv_loc, na_values="-1")
        dummy_df[image_name] = df['y']
    dummy_df = dummy_df.set_index("x").transpose().fillna(-1).astype('int64')
    dummy_df["Image name"] = dummy_df.index
    merge_df = pd.merge(used_images_info, dummy_df, how="inner", on="Image name")

    merge_df["Date Time, GMT-07:00"] = pd.to_datetime(merge_df["Date Time, GMT-07:00"],
                                                      format='%m/%d/%y %I:%M:%S  %p')
    merge_df.sort_values(by=["Date Time, GMT-07:00"], inplace=True)
    for i in range(image_width):
        output_df = merge_df[["Date Time, GMT-07:00", i]]
        output_df = output_df.rename(columns={i: "y"})
        output_df[["Date Time, GMT-07:00", "y"]].to_csv(os.path.join(f"coord_by_horizontal_profile/{images_director}",
                                                                     f'lake_level_{i}_profile.csv')
                                                        , index=False, na_rep='-1')


if __name__ == '__main__':

    marked_color = (255, 0, 255)  # magneta
    '''
    image_width = 7392
    images_dir = "decrease"
    images_info = pd.read_csv("KW_lowerlake_2023.csv")
    marked_color = (255, 0, 255)  # magneta
    extract_coord_by_image(images_dir, marked_color)
    create_coord_by_horizontal_profiles(images_dir, images_info, image_width)
    images_dir = "increase"
    extract_coord_by_image(images_dir, marked_color)
    create_coord_by_horizontal_profiles(images_dir, images_info, image_width)
    '''
    images_info = pd.read_csv("KW_lowerlake_2022.csv")
    images_dir = "2022_seawall"
    image_width = 5888
    extract_coord_by_image(images_dir, marked_color)
    create_coord_by_horizontal_profiles(images_dir, images_info, image_width)
