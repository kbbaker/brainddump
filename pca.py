__author__ = 'Kevin'

from sklearn.decomposition import PCA
from osgeo import ogr

streets = ogr.Open('osm_roads_ovl.shp', update = 1)
streetsLayer = streets.GetLayer()

f = open('clusters.txt', 'w')

features = []
keys = []
for feature in streetsLayer:
    output = []
    keys.append(feature.GetField('osm_id'))
    for field in ['0','1','2','3','4','5', 'SUM']:
        out = feature.GetField(field)
        if out == None:
            output.append(0)
        else:
            output.append(out)
    features.append(output)

pca = PCA(n_components=2)
pca.fit(features)

print(pca.explained_variance_ratio_)