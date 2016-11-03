from pymongo import MongoClient
from os.path import join, dirname
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from collections import OrderedDict

class UserUserCollaborativeFiltering:
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
        self.__billings = billings
        self.__customers = customers
        self.__items = items
        self.__args = args
        self.__metrics = {'accuracies': []}

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
        customers = np.array(self.__customers)
        items = np.array(self.__items)
        items_count = len(items)

        cf_matrix = pd.DataFrame(data=0 * items_count, index=customers, columns=items, dtype=float)

        return cf_matrix

    def train(self):
        billing_count = self.__billings.count()

        divider = float(billing_count) / self.__args.kfold
        accuracy = 0

        for k in xrange(1, self.__args.kfold + 1):
            skip = int(k * divider)
            ## split the data
            test_sample = self.__billings[:skip]
            target_sample = self.__billings[skip + 1:]

            cf_matrix = self.fit_cf_matrix(target_sample)
            accuracy += self.__calculate_neighbors_fold(test_sample, cf_matrix)

        accuracy = (accuracy/self.__args.kfold) * 100

    def __calculate_neighbors_fold(self, test_sample, cf_matrix):
        # verify
        accuracy = 0
        for test_document in test_sample:
            item_code_test = test_document.get('produto').get('codigo')
            customer_code_test = test_document.get('cliente').get('codigo')
            # get the item by the row, since its indexed by item
            target_features_test = np.array([cf_matrix.loc[customer_code_test].values])

            distances, indexes = self.__find_knn(cf_matrix, target_features_test)
            # asure that the array contains on index nearest neighbors indexes
            indexes = [i for i in indexes[0] if self.__customers[i] != customer_code_test]
            accuracy += self.__calculate_acuracy(indexes, customer_code_test, cf_matrix)

        return accuracy/test_sample.count()

    def __get__most_voted_items(self, indexes, cf_matrix):
        items_votes = {}
        for i in indexes:
            neighbor_code = self.__customers[i]
            neighbor = cf_matrix.loc[neighbor_code]

            for item in neighbor.index:
                if neighbor[item] > 0:
                    if item not in items_votes.keys():
                        items_votes[item] = 1
                    else:
                        items_votes[item] += 1

        return self.vote(items_votes)

    def vote(self, items_votes):
        #sort the most voted items
        items_votes = OrderedDict(sorted(items_votes.items(), key=lambda x: x[1]))
        top_items = items_votes.keys()

        size = len(top_items)
        first_index = size - self.__args.top_items

        #split the top items till top_items_threashold
        top_items = top_items[first_index:]

        top_items.reverse()

        return top_items

    def __calculate_acuracy(self, indexes, customer_code, cf_matrix):
        most_voted_items = self.__get__most_voted_items(indexes, cf_matrix)
        test_items = set(cf_matrix.loc[customer_code].index)

        hits = set(most_voted_items).intersection(test_items)

        accuracy = len(hits)/test_items

        return accuracy

    def get_metrics(self):
        return self.__metrics

    def fit_cf_matrix(self, target_sample):
        cf_matrix = self.__init_cf_matrix()

        # veryfied
        for target_document in target_sample:
            rating = target_document.get('valorLiquido')
            customer_code = target_document.get('cliente').get('codigo')
            item_code = target_document.get('produto').get('codigo')
            cf_matrix.loc[customer_code][item_code] += rating

        return cf_matrix

    def __find_knn(self, cf_matrix, target_features):
        neighbors = NearestNeighbors(n_neighbors=self.__args.n_neighbors, algorithm=self.__args.alg).fit(
            cf_matrix.values)
        distances, indexes = neighbors.kneighbors(target_features)
        return distances, indexes
