from typing import Tuple

import numpy as np
import cv2 as cv
import glob
from pathlib import Path


def camera_calibration(image_fname, grid_pattern: Tuple[int, int], show_image_result=False):
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    flags = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE
    objp = np.zeros((grid_pattern[1] * grid_pattern[0], 3), np.float32)
    objp[:, :2] = np.mgrid[0:grid_pattern[0], 0:grid_pattern[1]].T.reshape(-1, 2)
    file_stem = Path(fname).stem

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    image = cv.imread(image_fname)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(gray, grid_pattern, flags=flags)

    if ret:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        if show_image_result:
            # Draw and display the corners
            cv.drawChessboardCorners(image, grid_pattern, corners2, ret)
            cv.imshow('img', cv.resize(image, (2000, 1000)))
            cv.waitKey(0)

        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        h, w = image.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

        dst = cv.undistort(image, mtx, dist, None, newcameramtx)
        # crop the image
        x, y, w, h = roi
        # dst = dst[y:y + h, x:x + w]
        cv.imwrite(f'recalibrated_image/{file_stem}_recalib.png', dst)

        mean_error = 0
        for i in range(len(objpoints)):
            imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
            mean_error += error
        print(f"{file_stem} total error: {format(mean_error / len(objpoints))}")

        fx = mtx[0][0]
        fy = mtx[1][1]
        cx = mtx[0][2]
        cy = mtx[1][2]

        # output to text
        output_file = f'calib_info/{file_stem}_calib.txt'
        with open(output_file, 'w') as f:
            f.write(f'RadialDistortion\n[{dist[0][0]}\t{dist[0][1]}\t{dist[0][4]}]\n'
                    f'TangentialDistortion\n[{dist[0][2]}\t{dist[0][3]}]\n'
                    f'IntrinsicMatrix\n[{fx}\t0.0\t0.0]\n'
                    f'[0.\t{fy}\t0.0]\n'
                    f'[{cx}\t{cy}\t1.0]\n'
                    f'End')
    else:
        print("Fail to calibrate image")


if __name__ == '__main__':
    folder_input = 'calibration_image'
    grid = (9, 6)
    images = glob.glob(f'{folder_input}/*.JPG')
    for fname in images:
        camera_calibration(fname, grid, False)
