from sklearn import datasets
import numpy as np
import pandas as pd

data = np.load(fname='data.csv', delimiter=',')

for d in data:
    print(d)

