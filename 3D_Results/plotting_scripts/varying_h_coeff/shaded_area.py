from scipy.interpolate import interp2d, RectBivariateSpline
from scipy.spatial import ConvexHull
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

import matplotlib.pyplot as plt

import numpy as np


def get_internal_points(X, Y, Z, sampling_size=200, min_value=0.5, max_value=None):
    interpolated_z = RectBivariateSpline(X, Y, Z)

    smooth_x = np.linspace(X.min(), X.max(), num=sampling_size)
    smooth_y = np.linspace(Y.min(), Y.max(), num=sampling_size)

    smooth_z = interpolated_z(smooth_x, smooth_y)
    smooth_xx, smooth_yy = np.meshgrid(smooth_x, smooth_y)

    if not max_value:
        max_value = Z.max()
    if not min_value:
        max_value = Z.min()
    indexes_shaded_pts = np.where(
        (smooth_z >= min_value) & (smooth_z <= max_value)
    )  # criteria
    safety_factor = 1.01
    indexes_above_max = np.where(smooth_z > max_value * safety_factor)

    shaded_XX = smooth_xx[indexes_shaded_pts]
    shaded_YY = smooth_yy[indexes_shaded_pts]

    shaded_points = np.vstack([shaded_XX.ravel(), shaded_YY.ravel()])
    shaded_points = np.concatenate(
        [shaded_points[0][:, None], shaded_points[1][:, None]], axis=1
    )

    hollow_XX = smooth_xx[indexes_above_max]
    hollow_YY = smooth_yy[indexes_above_max]

    hollow_points = np.vstack([hollow_XX.ravel(), hollow_YY.ravel()])
    hollow_points = np.concatenate(
        [hollow_points[0][:, None], hollow_points[1][:, None]], axis=1
    )
    return shaded_points, hollow_points


def shaded_area(
    X, Y, Z, sampling_size=200, min_value=0.5, max_value=None, **patch_kwargs
):
    shaded_points, hollow_points = get_internal_points(
        X, Y, Z, sampling_size=sampling_size, min_value=min_value, max_value=max_value
    )
    hull_outer = ConvexHull(shaded_points)

    outer_points = np.concatenate(
        [
            shaded_points[hull_outer.vertices, 0][:, None],
            shaded_points[hull_outer.vertices, 1][:, None],
        ],
        axis=1,
    )
    total_points = np.concatenate(
        (
            outer_points,
            [outer_points[0]],
        )
    )
    if hollow_points.size > 0:
        hull_inner = ConvexHull(hollow_points)
        inner_points = np.concatenate(
            [
                hollow_points[hull_inner.vertices, 0][:, None],
                hollow_points[hull_inner.vertices, 1][:, None],
            ],
            axis=1,
        )
        total_points = np.concatenate(
            (total_points, [inner_points[0]], inner_points[::-1])
        )

    polygons = [Polygon(total_points)]
    p = PatchCollection(polygons, **patch_kwargs)
    plt.gca().add_collection(p)
