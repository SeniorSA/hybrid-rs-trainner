import os.path
import pandas as pd
import numpy as np

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

__location__ = __location__ + '/data/' + 'billings-data.csv'

data_frame = pd.read_csv(__location__)

from pymongo import MongoClient

client = MongoClient()
db = client.testando

cs = np.array(['c1', 'c2', 'c3', 'c4'])
its = np.array(['p1', 'p2', 'p3'])
data = np.array([[10, 20, 30],
                 [50, 60, 70],
                 [1000, 2230, 330],
                 [1033300, 22130, 3430]])


data_frame = pd.DataFrame(data=data, columns=its, index=cs, dtype=str)


print data_frame

# ant = data_frame[0:][0:].values
# print ant


# pd.data_frame = pd.DataFrame(data=np.array(2531))
