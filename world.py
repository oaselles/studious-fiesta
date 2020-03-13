from libpysal.cg.voronoi import voronoi, voronoi_frames
from libpysal.weights import Queen

import numpy as np
import random

from shapely.geometry import Point, box

import geopandas as gpd
import pandas as pd

np.random.seed(12345)


def sample_points(sample_geometry, n_points):
    points = list()
    minx, miny, maxx, maxy = sample_geometry.bounds
    while len(points) < n_points:
        p = Point((random.uniform(minx, maxx), random.uniform(miny, maxy)))
        if p.within(sample_geometry):
            points.append([p.x, p.y])
    return points


class Agent:

    def __init__(self, **attrs):
        self.time = 0
        self.attrs = attrs
        self.agents = list()
        self.parent = False

        self._statelog = list()

    def run(self, state={}):
        self.time += 1
        self._run()
        for agent in self.agents:
            agent.run()
        return state


class MapUnit(Agent):
    def __init__(self, size=None, geometry=None, **args):
        Agent.__init__(self, **args)

        if size:
            self.geometry = box(0, 0, size[0], size[1])
        else:
            self.geometry = geometry

    @property
    def regions(self):
        return [r for r in self.agents if isinstance(r, MapUnit)]

    def plot_regions(self, ax=None, color=None):
        gdf = gpd.GeoSeries([a.geometry for a in self.regions])
        ax = gdf.plot(ax=ax, color=color)
        return ax

    def _regiontree(self, region_list=None):

        if region_list is None:
            region_list = list()

        if self.regions:
            for region in self.regions:
                region_list = region._regiontree(region_list)
        else:
            region_list.append(self.geometry)

        return region_list

    def build_regions(self, n_points=50, depth=1):
        points = sample_points(self.geometry, n_points)

        # regions, vertices = voronoi(points)
        regions_df, points_df = voronoi_frames(points)

        # clip regions to map unit
        regions_df = regions_df.assign(
            geometry=regions_df.geometry.intersection(self.geometry))

        self.agents = regions_df.geometry.apply(
            lambda x: MapUnit(geometry=x)).tolist()

        depth -= 1
        if depth > 0:
            for agent in self.regions:
                agent.build_regions(n_points=n_points, depth=depth)


m = MapUnit((100, 100))
m.build_regions(depth=1)

# n_points = 200
# np.random.seed(12345)
# points = np.random.random((n_points, 2)) * 10

# mins = points.min(axis=0)
# maxs = points.max(axis=0)

# regions, vertices = voronoi(points)
# regions_df, points_df = voronoi_frames(points)

# # flood ocean (borders and then random floods)
# bounds = box(*regions_df.total_bounds)

# # lakes (seed lakes and grow using allocated)
# prop_lakes = 0.1
# lake_cluster = 0.6


# w = Queen.from_dataframe(regions_df)


# def dist_from_center(points_df):
#     x = points_df.geometry.x.mean()
#     y = points_df.geometry.y.mean()
#     center = Point(x, y)
#     points_df = points_df.assign(dist_center=points_df.distance(center))
#     return points_df


# points_df = dist_from_center(points_df)
