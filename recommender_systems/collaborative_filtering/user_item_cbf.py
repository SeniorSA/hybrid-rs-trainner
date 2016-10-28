from pymongo import MongoClient
from os.path import join, dirname
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors


class UserItemCollaborativeFiltering:

    """The billings args should be pass a billings matrix like:
        - a list of dicts which should contains the keys:
         > a str customer_code (representing the customer identifier)
         > a str item_code (representing the item identifier)
         > a float rating (represeting the rating which the knn based methods will use to calculate de similarity between the customers)
        - it should look like this:
            [{'customer_code': 'c1', 'item_code': 'i1', 'rating': 0}]
    """
    def __init__(self, args, billings, customers, items):
        self.__validate_params(args, billings, customers, items)
        self.billings = billings
        self.customers = customers
        self.items = items

    def __validate_params(self, args, billings, customers, items):
        if billings == None or len(billings) > len(customers) * len(items):
            raise Exception('billings data source invalid')

        if customers == None:
            raise Exception('customers data source invalid')

        if items == None:
            raise Exception('items data source invalid')

        if args == None:
            raise Exception

    def __init_cf_matrix(self):
        customers = np.array(self.customers)
        items = np.array(self.items)
        items_count = len(items)

        cf_matrix = pd.DataFrame(data=0 * items_count, index=customers, columns=items, dtype=float)

        return cf_matrix

    def train(self):
        billing_count = len(self.billings)

        divider = float(billing_count) / self.args.kfold
        for k in xrange(1, self.args.kfold + 1):
            skip = int(k * divider)
            ## split the data
            test_sample = self.billings[:skip]
            target_sample = self.billings[skip + 1:]

            cf_matrix = self.fit_cf_matrix(target_sample)
            self.__calculate_neighbors(test_sample, cf_matrix)

    def __calculate_neighbors(self, test_sample, cf_matrix):
        for test_document in test_sample:
            item_code = test_document.get('item_code')
            customer_code = test_document.get('customer_code')
            # get the item by the row, since its indexed by item
            target_features = cf_matrix.loc[customer_code].values

            nearest_neighbors = self.__find_knn(cf_matrix, target_features)
            self.__validate_neighbors(nearest_neighbors, cf_matrix)

    def __validate_neighbors(self, nearest_neighbors, cf_matrix):
        for neighbor in nearest_neighbors:
            print neighbor

    def fit_cf_matrix(self, target_sample):
        cf_matrix = self.__init_cf_matrix()

        #veryfid
        for target_document in target_sample:
            rating = target_document.get('rating')
            customer_code = target_document.get('customer_code')
            item_code = target_document.get('item_code')
            cf_matrix[customer_code][item_code] += rating

        return cf_matrix

    def __find_knn(self, cf_matrix, target_features):
        neighbors = NearestNeighbors(n_neighbors=self.args.n_neighbors, algorithm=self.args.alg).fit(cf_matrix.values)
        distances, indexes = neighbors.kneighbors(target_features)

        return distances, indexes
