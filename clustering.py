__author__ = 'Kevin'

from sklearn import cluster, datasets
from osgeo import ogr

streets = ogr.Open('osm_roads_ovl.shp', update = 1)
streetsLayer = streets.GetLayer()

f = open('clusters.txt', 'w')

features = []
keys = []
for feature in streetsLayer:
    output = []
    keys.append(feature.GetField('osm_id'))
    for field in ['6_top', '6_bottom', '7_top', '7_bottom', '5_top', '5_bottom']:
        out = feature.GetField(field)
        if out == None:
            output.append(0)
        else:
            output.append(out)
    features.append(output)

k_means = cluster.KMeans(n_clusters=5)
k_means.fit(features)

for i, cluster in enumerate(k_means.labels_):
    f.write(str(keys[i]) + ';' + str(cluster) + ';' + ';'.join(map(str, features[i])) + '\n')

f.close()
