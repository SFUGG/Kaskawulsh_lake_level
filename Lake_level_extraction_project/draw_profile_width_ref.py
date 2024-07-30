import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker
import cv2 as cv
from pathlib import Path


def draw_ref(ref_image, profile_widths):
    fig = plt.figure(figsize=(16, 9))
    img_name = Path(ref_image).stem
    axes = plt.gca()
    img = cv.imread(ref_image, cv.IMREAD_COLOR)
    axes.imshow(img, alpha=0.8, interpolation='nearest', zorder=1)
    axes.xaxis.set_major_locator(ticker.MultipleLocator(profile_widths))
    axes.tick_params(axis='x', colors='blue')
    plt.grid(axis='x', which='major', color='blue')
    plt.xticks(fontsize=11)
    plt.grid(axis='x', which='major', linewidth=1, zorder=2)
    axes.get_yaxis().set_visible(False)
    plt.savefig(f"plot_result/ref_{img_name}_{profile_widths}.png", bbox_inches='tight')


if __name__ == '__main__':
    ref_image = "raw_data/raw_image/IM_00023.JPG"
    draw_ref(ref_image, 350)
    draw_ref(ref_image, 250)

    ref_image = "raw_data/raw_image/IM_00142.JPG"
    draw_ref(ref_image, 100)
    draw_ref(ref_image, 300)
