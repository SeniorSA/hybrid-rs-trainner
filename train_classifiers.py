from sklearn import datasets
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
import numpy as np
import pandas as pd
import csv
from os.path import join, dirname

module_path = dirname(__file__)

# iris = datasets.load_iris()

x = np.array([
    [2, 1],
    [-2, -1],
    [500, 1000],
    [1000, 3000]
])

y = np.array([
    [0, -5],
    [-2, -3],
    [123, 21],
    [100, 200]
])

neighbor = NearestNeighbors(metric='euclidean')
neighbor.fit(x)
a, b = neighbor.kneighbors([[1, 1]], n_neighbors=3)

print(a)
print(b)

# j = -1
# size = len(retorno[0])
# for i in xrange(0, size):
#     for j in xrange(0, size-1):
#         if (retorno[0][i] > retorno[0][j + 1]):
#             aux = retorno[0][i]
#             retorno[0][i] = retorno[0][j]
#             retorno[0][i] = aux
#
# for i in xrange(size):
#     print(int(i))



#
# def load_files():
#     module_path = dirname(__file__)
#     with open(join(module_path, 'data', 'clientes.csv')) as csv_file:
#         data_file = csv.reader(csv_file)
#         line = next(data_file)
#         n_samples = 14642
#         n_features = len(line)
#         data = np.empty((n_samples, n_features))
#         target = np.empty((n_samples,), dtype=np.int)
#
#         for i, ir in enumerate(data_file):
#             data[i] = np.asarray(ir[:-1], dtype=np.float64)
#             target[i] = np.asarray(ir[-1], dtype=np.int)
#
# ###calculate matrix distances###
#
# #load_files()
