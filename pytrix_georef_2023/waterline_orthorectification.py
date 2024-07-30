import numpy as np
import datetime
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.dates import DateFormatter
import matplotlib.image as mpimg
import pandas as pd
import sklearn
from sklearn.metrics import mean_squared_error

from PyTrx.CamEnv import GCPs, CamEnv, setProjection, projectUV, projectXYZ
from PyTrx.Images import CamImage

# =============================================================================
# Define camera projection
# =============================================================================

PERIOD = ['decrease', 'increase']
DEM_USED = ['glo', 'arctic']
CGP_OPTIMIZATION_SCHEME = ['org', 'opt1', 'opt2', 'opt3', 'opt4', 'opt5']
OPT_PARA = ['YPR', 'ALL']
OPT_METHOD = ['trf', 'dogbox', 'lm']

OPTIMIZATION_SCHEME = {
    'org': {
        'prefix': '',
        'para': 'YPR',
        'method': 'trf',
        'output': ''
    },
    'opt1': {
        'prefix': '_opt1',
        'para': 'YPR',
        'method': 'trf',
        'output': '_opt1'
    },
    'opt2': {
        'prefix': '_opt2',
        'para': 'YPR',
        'method': 'trf',
        'output': '_opt2'
    },
    'opt3': {
        'prefix': '_opt3',
        'para': 'YPR',
        'method': 'trf',
        'output': '_opt3'
    },
    'opt4': {
        'prefix': '_opt4',
        'para': 'YPR',
        'method': 'trf',
        'output': '_opt4'
    },
    'opt5': {
        'prefix': '_opt5',
        'para': 'YPR',
        'method': 'trf',
        'output': '_opt5'
    },
    'opt6': {
        'prefix': '',
        'para': 'YPR',
        'method': 'dogbox',
        'output': '_opt6'
    },
    'opt7': {
        'prefix': '',
        'para': 'YPR',
        'method': 'lm',
        'output': '_opt7'
    }

}


def georef(camenv, calibimg, gcps_files, df, optparams, optmethod, output):
    img = CamImage(calibimg)
    cam = CamEnv(camenv)
    dem = cam.getDEM()
    gcps = GCPs(dem, gcps_files, calibimg)
    y = 4159 - df['y'].to_numpy()
    xy = np.zeros((y.size, 2))
    xy[:, 1] = y
    xy[:, 0].fill(875)

    # Optimise camera environment
    cam.optimiseCamEnv(optparams, optmethod, show=True)

    # Report calibration data
    # cam.reportCalibData()

    # Get inverse projection variables through camera info
    invprojvars = setProjection(dem, cam._camloc, cam._camDirection,
                                cam._radCorr, cam._tanCorr,
                                cam._focLen, cam._camCen,
                                cam._refImage, viewshed=False)

    # Inverse project image coordinates using function from CamEnv object
    xyz = projectUV(xy, invprojvars)

    res = pd.DataFrame(xyz)
    res.columns = ['x', 'y', 'z']
    df['x_3d'] = res.x
    df['y_3d'] = res.y
    df['z'] = res.z
    df.to_csv(output, na_rep='-1', index=False)


if __name__ == '__main__':
    period = PERIOD[0]
    opt = 'opt8'
    optimization_scheme = OPTIMIZATION_SCHEME[opt]
    dem_used = DEM_USED[0]
    input_prefix = optimization_scheme["prefix"]
    output_prefix = optimization_scheme['output']

    ingleCamEnv = f'cam_data/camenv_{dem_used}{input_prefix}.txt'
    ingle_calibimg = 'cam_data/images/increase/IM_00025.JPG'
    # Get GCPs
    inglefield_gcps = f'cam_data/gcps_{dem_used}{input_prefix}.txt'
    # retrive x,y from csv
    df = pd.read_csv(f"csv_data/lake_level_750_999_{period}.csv", parse_dates=["Date Time, GMT-07:00"])
    georef(camenv=ingleCamEnv, calibimg=ingle_calibimg,
           gcps_files=inglefield_gcps, df=df,
           optparams=optimization_scheme["para"], optmethod=optimization_scheme["method"],
           output=f'csv_data/elevation_result_{period}_{dem_used}{output_prefix}.csv')
