import glob
from pathlib import Path

import cv2 as cv

def mass_resize(period):
    images_drs = glob.glob(f"Enlarged_marked/{period}/*.jpg")
    for images_dr in images_drs:
        image_name = Path(images_dr).stem
        image = cv.imread(images_dr, cv.IMREAD_COLOR)
        image_resize = cv.resize(image, (1848, 1040), interpolation=cv.INTER_CUBIC)
        output_dir = f"resize/{period}/{image_name}.jpg"
        cv.imwrite(output_dir, image_resize)

if __name__ == '__main__':
    mass_resize('2022')