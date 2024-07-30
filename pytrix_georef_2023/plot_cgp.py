from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.transforms
import cv2 as cv

cgp = pd.read_csv("csv_data/cgp.csv")
ref_image = cv.imread("cam_data/images/increase/IM_00025.JPG", cv.IMREAD_COLOR)
for num in range(0, 10):
    x = int(cgp.iloc[num, 1])
    y = int(cgp.iloc[num, 2])
    cv.circle(ref_image, (x, y), 10, (0, 0, 255), -1)
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(ref_image, f'{num + 1}', (x + 30, y), font, 10, (0, 0, 255), 10, cv.LINE_AA)
cv.imwrite("cam_data/ref_cgp.jpeg", ref_image)
