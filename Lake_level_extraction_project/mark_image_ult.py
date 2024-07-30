from pathlib import Path

import cv2 as cv
import pandas as pd
import numpy as np
import glob


def enlarged_marked(ref_image, marked_value, half_width, output_dir):
    marked_pos = np.where(np.all(ref_image == marked_value, axis=-1))
    marked_band = np.repeat(np.reshape(marked_value, (1, 3)), marked_pos[0].shape[0], 0)
    for i in range(1, half_width):
        ref_image[marked_pos[0] + i, marked_pos[1], :] = marked_band
        ref_image[marked_pos[0] - i, marked_pos[1], :] = marked_band

    cv.imwrite(output_dir, ref_image)

def mass_draw(dir, period, width):
    images_drs = glob.glob(f'{dir}/{period}/*.png')
    for images_dr in images_drs:
        image_name = Path(images_dr).stem
        image = cv.imread(images_dr, cv.IMREAD_COLOR)
        output_dir = f"Enlarged_marked/{period}/{image_name}.jpg"
        enlarged_marked(image, (255, 0, 255), width, output_dir)

def horizontal_draw(ref_image, marked_value, start_profiles, end_profiles, num_profiles, output_dir):
    bands = np.arange(start=start_profiles, stop=end_profiles, step=num_profiles)
    for horizontal_band in bands:
        ref_image = cv.line(ref_image, (horizontal_band, 0), (horizontal_band, ref_image.shape[0]), marked_value, 4)
    ref_image = cv.line(ref_image, (end_profiles, 0), (end_profiles, ref_image.shape[0]), marked_value, 4)
    cv.imwrite(output_dir, ref_image)


if __name__ == '__main__':
    mass_draw(f"Marked_photo", 'increase', 4)
    mass_draw(f"Marked_photo", 'decrease', 4)
    mass_draw(f"Marked_photo", '2022', 4)
