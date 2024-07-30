from PIL import Image, ExifTags
import glob
from pathlib import Path
import pandas as pd
import numpy as np


def extract_datetime(input_folder, output_file):
    images_name = glob.glob(f'{input_folder}\\*.JPG')
    datetime_tag = 306  # Defined by PIL Exif Tag
    images_list = []
    datetime_list = []
    for fname in images_name:
        img = Image.open(fname)
        img_exif = img.getexif()
        images_list.append(Path(fname).stem)

        if img_exif is not None:
            datetime_vals = img_exif[datetime_tag]
            datetime_list.append(datetime_vals)
        else:
            datetime_list.append(np.nan)
    df = pd.DataFrame({
        "Image name": images_list, "Date Time": datetime_list
    })
    df["Date Time, GMT-07:00"] = pd.to_datetime(df["Date Time"], format='%Y:%m:%d %H:%M:%S')
    df.to_csv(output_file, columns=["Image name", "Date Time, GMT-07:00"],
              date_format='%m/%d/%y %I:%M:%S  %p', index=False)


if __name__ == '__main__':
    extract_datetime("D:\\Murphy\\Photo_data\\KW_lowerlake_2023\\PHOTO", "KW_lowerlake_2023.csv")
    extract_datetime("D:\\Murphy\\Photo_data\\KW_lowerlake_2022\\PHOTO", "KW_lowerlake_2022.csv")


