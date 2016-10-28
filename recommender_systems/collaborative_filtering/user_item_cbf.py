from pymongo import MongoClient
from os.path import join, dirname
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors


class UserItemCollaborativeFiltering:
    """ * billings args should be pass a billings matrix like:
            - a list of dicts which should contains the keys:
            > a str customer_code (representing the customer identifier)
            > a str item_code (representing the item identifier)
            > a float rating (represeting the rating which the knn based methods will use to calculate de similarity between the customers)
                - it should look like this:
                [{'customer_code': {'codigo': 'c1'}, 'item_code': 'i1', 'rating': 0}]
        * customers args should be an array of str representing the customer ID
        * items args should be an array of str representing the item ID
    """

    def __init__(self, args, billings, customers, items):
        self.__validate_params(args, billings, customers, items)
        self.billings = billings
        self.customers = customers
        self.items = items
        self.args = args

    def __validate_params(self, args, billings, customers, items):
        if billings == None or billings.count() > len(customers) * len(items):
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
        billing_count = self.billings.count()

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
            item_code = test_document.get('produto').get('codigo')
            customer_code = test_document.get('cliente').get('codigo')
            # get the item by the row, since its indexed by item
            target_features = np.array([cf_matrix.loc[customer_code].values])

            distances, indexes = self.__find_knn(cf_matrix, target_features)
            self.__validate_fold(distances, indexes, test_sample)

    def __validate_fold(self, distances, indexes, test_sameple):
        # I don't know for sure if always return a matrix like [0] x N, where N its the number of neighbors.
        # If returns more than [0] n N, something like [1] x N, then this method should be rewrited.
        count = 0
        indexes = indexes[0]
        for i in indexes:
            customer_code = self.customers[i]
            for test in test_sameple:
                cliente_codigo = test.get('cliente').get('codigo')
                if cliente_codigo == customer_code:
                    count += 1

        ##generate the log
        accuracy = (float(count) / float(len(indexes))) * 100

    def fit_cf_matrix(self, target_sample):
        cf_matrix = self.__init_cf_matrix()

        # veryfid
        for target_document in target_sample:
            rating = target_document.get('valorLiquido')
            customer_code = target_document.get('cliente').get('codigo')
            item_code = target_document.get('produto').get('codigo')
            cf_matrix.loc[customer_code][item_code] += rating

        return cf_matrix

    def __find_knn(self, cf_matrix, target_features):
        neighbors = NearestNeighbors(n_neighbors=self.args.n_neighbors, algorithm=self.args.alg).fit(cf_matrix.values)
        distances, indexes = neighbors.kneighbors(target_features)
        return distances, indexes
