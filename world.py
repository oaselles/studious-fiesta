from libpysal.cg.voronoi import voronoi, voronoi_frames
from libpysal.weights import Queen

# class Place(object):
#     def __init__(self):
#         self.name = None
#         self.geometry = None
#         self.places = list()

#      def build(self):
#      	pass

# class Settlement(Place):
#     def __init__(self):
#         pop = 100

n_points = 500
np.random.seed(12345)
points = np.random.random((n_points, 2)) * 10 + 10

mins = points.min(axis=0)
maxs = points.max(axis=0)

regions, vertices = voronoi(points)
regions_df, points_df = voronoi_frames(points)

w = Queen.from_dataframe(regions_df)
