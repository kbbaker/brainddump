__author__ = 'Kevin'

import matplotlib.pyplot as plt
from osgeo import ogr
from sklearn.neighbors import KernelDensity
from scipy.stats import norm
import numpy as np
import pickle


'''streets = ogr.Open('SQLExecutor_Result_line.shp', update = 1)
streetsLayer = streets.GetLayer()

features = [[],[],[],[],[],[],[]]
keys = []
for feature in streetsLayer:
    #keys.append(feature.GetField('osm_id'))
    #for i, field in enumerate(['6_top', '6_bottom', '7_top', '7_bottom', '5_top', '5_bottom', 'speed_b']):
    for i, field in enumerate(['speed_b']):
        out = feature.GetField(field)
        if out == None:
            features[i].append(0)
        else:
            features[i].append(out)

#pickle.dump( features, open( "features.p", "wb" ) )'''
features = pickle.load(open( "features.p", "rb" ))

print "features read"

'''X = np.vstack(features[5])

X_plot = np.linspace(0, 40, 1000)[:, np.newaxis]
mean = round(np.mean(X),4)
median = round(np.median(X),4)
'''
a = np.array(map(int,features[0]))
new_a = a[~((a < 1))]
percentiles = []

for i in range (0,100,5):
    percentiles.append(np.percentile(new_a, i))

print zip(range (0,100,5),percentiles)

'''fig, ax = plt.subplots()

kde = KernelDensity(kernel='gaussian', bandwidth=0.75).fit(X)
log_dens = kde.score_samples(X_plot)
ax.plot(X_plot[:, 0], np.exp(log_dens), '-', label="kernel = '{0}'".format('gaussian'))
ax.plot(X[:, 0], -0.005 - 0.01 * np.random.random(X.shape[0]), '+k')
#ax.vlines(mean,-0.02,0.4, colors = 'r')
#ax.vlines(median,-0.02,0.4, colors = 'b')
#ax.set_xlim(0,50)
#ax.set_ylim(-0.02, 0.8)'''

#plt.show()