from pymongo import MongoClient
from os.path import join, dirname
import numpy as np
import pandas as pd
from collections import OrderedDict

from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error, explained_variance_score, \
    accuracy_score, average_precision_score, f1_score, precision_score, recall_score, hamming_loss, hinge_loss, \
    jaccard_similarity_score, log_loss, matthews_corrcoef, cohen_kappa_score


class UserUserCollaborativeFiltering:
    """ * the args params should be an namespace ... [to be continued]
        * the data param should contain a pandas dataframe containing where the row (index) should be users and columns should be a item.
            the value data.loc['user1'].values should conting  the ratings about the items
    """

    def __init__(self, args, data):
        self.__validate_params(args, data)
        self.__args = args
        self.data = data
        self.list_index = list(data.index)
        self.__metrics = []

    def __validate_params(self, args, data):
        if data == None:
            raise Exception

        if args == None:
            raise Exception

    def train(self):
        billing_count = len(self.data)

        divider = float(billing_count) / self.__args.kfold
        accuracies = []

        for k in xrange(1, self.__args.kfold + 1):
            skip = int(k * divider)
            ## split the data

            test_sample = self.data.iloc[:skip]
            cf_target_sample = self.data.iloc[skip + 1:]

            accuracies.push(self.__calculate_neighbors_fold(test_sample, cf_target_sample))

        max_accuracy = max(accuracies)
        best_test_index = accuracies.index(max_accuracy)
        self.__choose_best_fold(best_test_index)

    def __choose_best_fold(self, test_fold_index):
        before_test_index = self.data.iloc[:test_fold_index]
        after_test_index = self.data.iloc[test_fold_index+1:]
        full_data = pd.concat([before_test_index, after_test_index])
        self.data = full_data

    def __calculate_neighbors_fold(self, test_sample, cf_target_sample):
        accuracy = 0.0

        for test_index in test_sample.index:
            # get the item by row, since its indexed by row
            target_features_test = test_sample.loc[test_index].values

            # get the nearest neighbors
            distances, neighbors_indexes = self.__find_knn(cf_target_sample, target_features_test)

            # asure that the array contains on index nearest neighbors indexes
            customer_index = self.list_index.index(test_index)
            neighbors_indexes = [i for i in neighbors_indexes[0] if i != customer_index]

            accuracy += self.calculate_metrics(neighbors_indexes, test_sample.loc[test_index].values, cf_target_sample)

        return accuracy / float(len(test_sample.index))

    def __get__most_voted_items(self, indexes, cf_matrix):
        items_votes = {}

        # generate the items array with zero ratings
        for item in self.data.columns:
            items_votes[item] = 0

        # for each neighbor in neighborhood, sum the items ratings that appears in the neighbor item sample (those who was rated by a neighbor)
        for i in indexes:
            item_ratings = self.data.iloc[i]

            for item_key in item_ratings:
                items_votes[item_key] += item_ratings[item_key]

        # return self.vote(items_votes, len(self.data.columns))
        return items_votes.values()

    """ * return most voted items based on ratings
    """

    # def vote(self, items_votes, threashold=None):
    #     # sort the most voted items
    #     items_votes = OrderedDict(sorted(items_votes.items(), key=lambda x: x[1]))
    #
    #     top_items = items_votes.keys()
    #
    #     size = len(top_items)
    #     if threashold == None:
    #         threashold = self.__args.top_items
    #
    #     first_index = size - threashold
    #
    #     # split the top items till top_items_threashold
    #     top_items = top_items[first_index:]
    #
    #     top_items.reverse()
    #
    #     return top_items

    def calculate_metrics(self, indexes, expected_ratings, cf_matrix):
        # metrics = {}
        # get most voted items
        predicted_ratings = self.__get__most_voted_items(indexes, cf_matrix)

        recall, accuracy, precision, f1 = self.calculate_classification_metrics(expected_ratings, predicted_ratings)
        # metrics['recall_score'] = recall
        # metrics['accuracy_score'] = accuracy
        # metrics['precision_score'] = precision
        # metrics['f1_score'] = f1
        #
        # mae, mse, median_ae, evs = self.calculate_regression_metrics(expected_ratings, predicted_ratings)
        # metrics['mean_absolute_error'] = mae
        # metrics['mean_squared_error'] = mse
        # metrics['median_absolute_error'] = median_ae
        # metrics['explained_variance_score'] = evs

        return accuracy

    def calculate_classification_metrics(self, expected, predicted):
        recall = recall_score(expected, predicted)
        accuracy = accuracy_score(expected, predicted)
        precision = precision_score(expected, predicted)
        f1 = f1_score(expected, predicted)

        return recall, accuracy, precision, f1
        # cohen_kappa = cohen_kappa_score(expected, predicted)
        # hamming = hamming_loss(predicted, expected)
        # jaccard = jaccard_similarity_score(expected, predicted)
        # logloss = log_loss(expected, predicted)
        # matthews = matthews_corrcoef(expected, predicted)

    def calculate_regression_metrics(self, expected, predicted):
        mae = mean_absolute_error(expected, predicted)
        mse = mean_squared_error(expected, predicted)
        median_ae = median_absolute_error(expected, predicted)
        evs = explained_variance_score(expected, predicted)

        return mae, mse, median_ae, evs

    def get_metrics(self):
        return self.__metrics

    def __find_knn__find_knn(self, target_matrix, target_features):
        neighbors = NearestNeighbors(n_neighbors=self.__args.n_neighbors, algorithm=self.__args.alg).fit(
            target_matrix.values)
        distances, indexes = neighbors.kneighbors(target_features)
        return distances, indexes
