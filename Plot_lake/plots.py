# importing libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import gridspec
from matplotlib.cm import ScalarMappable
from scipy.interpolate import (griddata, CubicSpline, Akima1DInterpolator,
                               PchipInterpolator, KroghInterpolator, BarycentricInterpolator)
import matplotlib.ticker as ticker



def plot_contour(x, y, z, resolution=30, contour_method='linear'):
    resolution = str(resolution) + 'j'
    X, Y = np.mgrid[min(x):max(x):complex(resolution), min(y):max(y):complex(resolution)]
    # X, Y = np.meshgrid(x, y)
    points = [[a, b] for a, b in zip(x, y)]
    Z = griddata(points, z, (X, Y), method=contour_method)
    return X, Y, Z


def plot_dem(xyz):
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    x = xyz.x.to_numpy()
    y = xyz.y.to_numpy()
    z = xyz.z.to_numpy()
    # XX, YY, ZZ = plot_contour(x, y, z, resolution=1749)

    XX = xyz.x.to_numpy().reshape((53, 33), order='F')
    YY = xyz.y.to_numpy().reshape((53, 33), order='F')
    ZZ = xyz.z.to_numpy().reshape((53, 33), order='F')
    vmin = 960
    vmax = 1000
    levels = 20
    level_boundaries = np.linspace(vmin, vmax, levels + 1)
    quadcontourset = ax.contourf(XX, YY, ZZ, vmin=vmin, vmax=vmax, levels=level_boundaries)
    plt.title("Elevation of Lower Lake using Sept2018 DEM", fontsize=18)
    legend = fig.colorbar(
        ScalarMappable(norm=quadcontourset.norm, cmap=quadcontourset.cmap),
        ax=ax,
        ticks=range(vmin, vmax + 5, 5),
        boundaries=level_boundaries,
        values=(level_boundaries[:-1] + level_boundaries[1:]) / 2,
    )
    legend.ax.set_ylabel('Elevation (m a.s.l.)', rotation=270, fontsize=14, labelpad=25)
    legend.ax.tick_params(labelsize=16)

    plt.xlabel('Easting (m)', fontsize=14)
    plt.ylabel('Northing (m)', fontsize=14)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.tight_layout()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig("lower_lake_sept2018.png")


def plot_elevation_by_northing(xz, xyz):
    y = xz.y.iat[0]

    x = xz.x.to_numpy()
    z = xz.z.to_numpy()

    fig = plt.figure(figsize=(12, 12), layout="constrained")
    ax1 = fig.add_subplot(211)
    ax1.plot(x, z, 'o--')
    ax1.set_xlabel('Northling (m)', fontsize=14)
    ax1.set_ylabel('Height above mean sea level (m)', fontsize=14)

    ax1.set_title(f"Elevation profile at {y} Northling, from {x.min()} to {x.max()} Eastling", fontsize=18)
    ax1.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    XX = xyz.x.to_numpy().reshape((53, 33), order='F')
    YY = xyz.y.to_numpy().reshape((53, 33), order='F')
    ZZ = xyz.z.to_numpy().reshape((53, 33), order='F')

    ax2 = fig.add_subplot(212, sharex=ax1)
    cs2 = ax2.contourf(XX, YY, ZZ, cmap="viridis")
    ax2.plot(x, xz.y.to_numpy(), 'r-', label="Elevation profiles position")
    ax2.set_title("Elevation of Lower Lake using Sept2018 DEM", fontsize=18)
    ax2.legend()
    legend = plt.colorbar(cs2)
    legend.ax.set_ylabel('Elevation (m a.s.l.)', rotation=270, fontsize=14, labelpad=25)
    ax2.set_xlabel('Easting (m)', fontsize=14)
    ax2.set_ylabel('Northing (m)', fontsize=14)
    ax2.ticklabel_format(style='sci', axis='both', scilimits=(0, 0))
    legend.ax.tick_params(labelsize=16)
    plt.savefig(f'plot/elevation_{y}_northling.png')
    plt.close(fig)


def plot_elevation_by_easting(yz, xyz):
    x = yz.x.iat[0]

    y = yz.y.to_numpy()
    z = yz.z.to_numpy()
    fig = plt.figure(figsize=(18, 8))
    spec = gridspec.GridSpec(ncols=2, nrows=1, width_ratios=[1, 2])
    ax1 = fig.add_subplot(spec[0])
    ax1.plot(z, y, 'o--')
    ax1.set_ylabel('Northing (m)', fontsize=14)
    ax1.set_xlabel('Height above mean sea level (m)', fontsize=14)

    ax1.set_title(f"Elevation profile at {x} Easting\nfrom {y.min()} to {y.max()} Northling", fontsize=18)
    ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    XX = xyz.x.to_numpy().reshape((53, 33), order='F')
    YY = xyz.y.to_numpy().reshape((53, 33), order='F')
    ZZ = xyz.z.to_numpy().reshape((53, 33), order='F')

    ax2 = fig.add_subplot(spec[1], sharey=ax1)
    cs2 = ax2.contourf(XX, YY, ZZ, cmap="viridis")
    ax2.plot(yz.x.to_numpy(), y, 'r-', label="Elevation profiles position")
    ax2.set_title("Elevation of Lower Lake using Sept2018 DEM", fontsize=18)
    ax2.legend()
    legend = plt.colorbar(cs2)
    legend.ax.set_ylabel('Elevation (m a.s.l.)', rotation=270, fontsize=14, labelpad=25)
    ax2.set_xlabel('Easting (m)', fontsize=14)
    ax2.set_ylabel('Northing (m)', fontsize=14)
    ax2.ticklabel_format(style='sci', axis='both', scilimits=(0, 0))
    legend.ax.tick_params(labelsize=16)
    plt.savefig(f'plot/elevation_{x}_eastling.png')
    plt.close(fig)

    return


def create_elevation_profiles(xyz):
    xyz.groupby(["x"]).apply(plot_elevation_by_easting, xyz=xyz)
    xyz.groupby(["y"]).apply(plot_elevation_by_northing, xyz=xyz)


def hypsometric_curve_area(xyz, vmax, vmin, increment, resolution):
    def count_bellow(z, num):
        return z.loc[lambda x: x <= num].count()
    levels = np.arange(vmin, vmax + 1, increment)
    counts = []
    for level in levels:
        counts.append(count_bellow(xyz.z, level))
    areas = np.array(counts) * (resolution ** 2)
    areas = areas / 1000
    volumes = [areas[0] * increment]
    for idx, area in enumerate(areas[1:]):
        volumes.append(area * increment + volumes[idx])
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    # ax.set_xlim(-10, 250)
    # ax.set_xticks(range(0, 251, 10))
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    lin1 = ax.plot(areas, levels, '-', label='Hypsometric curve area')
    ax2 = ax.twiny()
    # ax2.set_xlim(-20, 500)
    # ax2.set_xticks(range(0, 501, 20))
    ax2.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    lin2 = ax2.plot(volumes, levels, '-r', label='Volume-elevation curve')
    # ax2.invert_xaxis()

    plt.grid(axis='y', which='major', linewidth=1)
    ax.grid(axis='y', which='minor', linewidth=0.2)
    ax.set_ylabel("Height above mean sea level (m)")
    ax.set_xlabel(r"Area ($10^{3}\,m^{2}$)")
    ax2.set_xlabel(r"Volume ($10^{3}\,m^{3}$)")

    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc=8)

    ax.grid()
    ax.set_title("Area–volume–elevation (AVE) curves from Sept2018 DEM", fontsize=16)
    plt.savefig('curve_sept2018', bbox_inches='tight')
    plt.close(fig)

    df = pd.DataFrame({ 'elevation (m)': levels, 'area (m^2)': areas, 'volumes (m^3)': volumes})
    df.to_csv('data/hypsometric_curve_area.csv', index=False)




if __name__ == '__main__':
    xyz_df = pd.read_csv('data/lake_GLO30.csv', names=["x", "y", "z"])
    plot_dem(xyz_df)
    # create_elevation_profiles(xyz_df)
    hypsometric_curve_area(xyz_df, 1000, 960, 1, 20)
