from pymongo import MongoClient
from os.path import join, dirname
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors


class UserItemCollaborativeFiltering:
    def __init__(self, args, data_source):
        if args == None:
            raise Exception
        self.__validate_params(args, data_source)
        self.args = args
        self.data_source = data_source

    def __validate_params(self, args, data_source):
        if ['customer', 'items', 'billings'] not in data_source.keys():
            raise Exception('the data source must contain ["customers", "items", "billings"]')

        if args == None:
            raise Exception("args can't be invalid.")

    def __init_cf_matrix(self):
        customers = np.array(self.data_source.get('customer'))
        items = np.array(self.data_source.get('items'))
        items_count = len(items)

        cf_matrix = pd.DataFrame(data=0 * items_count, index=items, columns=customers, dtype=float)

        return cf_matrix

    # its too much coupled
    def train(self):
        # billing_count = db.faturamento.count()
        billing_count = 1540

        divider = float(billing_count) / self.args.kfold
        for k in xrange(1, self.args.kfold + 1):
            skip = int(k * divider)
            test_sample = db.faturamento.find().limit(skip)
            target_sample = db.faturamento.find().skip(skip + 1)

            cf_matrix = self.fit_cf_matrix(target_sample)
            self.__calculate_neighbors(test_sample, cf_matrix)

    def __calculate_neighbors(self, test_sample, cf_matrix):
        for test_document in test_sample:
            item_code = test_document.get('produto').get('codigo')
            customer_code = test_document.get('cliente').get('codigo')
            # get the item by the row, since its indexed by item
            target_features = cf_matrix.loc[customer_code].values

            nearest_neighbors = self.__find_knn(cf_matrix, target_features)
            self.__validate_neighbors(nearest_neighbors, cf_matrix)

    def __validate_neighbors(self, nearest_neighbors, cf_matrix):
        for neighbor in nearest_neighbors:
            print neighbor

    def fit_cf_matrix(self, target_sample):
        cf_matrix = self.__init_cf_matrix()

        for target_document in target_sample:
            liquid_value = target_document.get('valorLiquido')
            customer_code = target_document.get('cliente').get('codigo')
            item_code = target_document.get('produto').get('codigo')
            cf_matrix[customer_code][item_code] += liquid_value

        return cf_matrix

    def __find_knn(self, cf_matrix, target_features):
        neighbors = NearestNeighbors(n_neighbors=args.n_neighbors, algorithm=args.alg).fit(cf_matrix.values)
        distances, indexes = neighbors.kneighbors(target_features)

        return distances, indexes
