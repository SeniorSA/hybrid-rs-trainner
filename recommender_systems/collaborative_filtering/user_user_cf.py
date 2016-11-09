from os.path import join, dirname
import logging
from collections import OrderedDict
import time
from sklearn.externals import joblib
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from recommender_systems.evaluation_metrics_utils import calculate_classification_metrics, calculate_regression_metrics

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create a file handler
current_time = time.localtime(time.time())
file_name = 'user_user_cf_knn-' + str(current_time.tm_mday) + '-' + str(current_time.tm_mon) + '-' + str(
    current_time.tm_year) + '-' + str(current_time.tm_hour) + '-' + str(current_time.tm_min) + '-' + str(
    current_time.tm_sec)
handler = logging.FileHandler(file_name + '.log')
handler.setLevel(logging.DEBUG)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)
logger.addHandler(streamHandler)


class UserUserCollaborativeFiltering:
    """ * the args params should be an namespace ... [to be continued]
        * the data param should contain a pandas dataframe containing where the row (index) should be users and columns should be a item.
            the value data.loc['user1'].values should conting  the ratings about the items
    """

    def __init__(self, args, data):
        self.__validate_params(args, data)
        self.__args = args
        self.cf_matrix = data
        self.list_index = list(data.index)
        self.__init_metrics()

    def __validate_params(self, args, data):
        if args == None:
            raise Exception

    def __init_metrics(self):
        self.__metrics = []
        for i in xrange(self.__args.kfold):
            self.__metrics.append({'recall_score': [], 'accuracy_score': [], 'precision_score': [], 'f1_score': []
                                      , 'mean_absolute_error': [], 'mean_squared_error': [],
                                   'median_absolute_error': [],
                                   'explained_variance_score': []})

    def __dump_args(self):
        logger.info('\n----------------- TRAINNING WITH PARAMS ----------------- ')
        logger.info('--alg %s' % self.__args.alg)
        logger.info('--n-neighbors %i' % self.__args.n_neighbors)
        logger.info('--kfold %i' % self.__args.kfold)
        logger.info('--distance-metric %s' % self.__args.distance_metric)
        logger.info('--p %i' % self.__args.p)
        logger.info('--leaf-size %i' % self.__args.leaf_size)
        logger.info('--weights %s' % self.__args.weights)

    def train(self):
        billing_count = len(self.cf_matrix)
        divider = float(billing_count) / self.__args.kfold
        accuracies = []
        training_folds = []

        self.__dump_args()

        for k in xrange(1, self.__args.kfold + 1):
            logger.info('\n*************** TRAINING TEST FOLD ***************%s ' % str(k))
            skip = int(k * divider)
            ## split the data

            first_index = int((k - 1) * divider)
            test_sample = self.cf_matrix.iloc[first_index:skip]

            after = self.cf_matrix.iloc[skip:]
            if first_index > 1:
                before = self.cf_matrix.iloc[:first_index]
                cf_target_sample = pd.concat([before, after])

            else:
                cf_target_sample = after

            training_folds.append(cf_target_sample)
            self.__calculate_neighbors_fold(test_sample, cf_target_sample, k)

        self.__choose_best_fold(training_folds)

    def __choose_best_fold(self, trainning_folds):
        ##calculate the average accuracy
        accuracies = []
        for metric in self.__metrics:
            acc = metric.get('accuracy_score')
            accuracies.append(np.mean(acc))
            # accuracy_std = np.std(acc)

        max_accuracy = max(accuracies)
        best_fold_index = accuracies.index(max_accuracy)
        self.cf_matrix = trainning_folds[best_fold_index]

        self.__dump_metrics(self.__metrics, best_fold_index)

        logger.info('---STARTING MODEL PERSISTENCE---')
        joblib.dump(self, file_name + '.pkl')
        logger.info('---FINISHED MODEL PERSISTENCE--')

    def predict(self, predicting_features):
        if predicting_features == None or len(predicting_features) < len(self.cf_matrix.columns):
            raise Exception

        distances, indexes = self.find_knn(target_matrix=self.cf_matrix, target_features=predicting_features)

        return self.predict_based_upon_neighbors(indexes, self.cf_matrix)

    def __calculate_neighbors_fold(self, test_sample, cf_target_sample, index):
        for test_index in test_sample.index:
            # get the item by row, since its indexed by row
            target_features_test = test_sample.loc[test_index].values

            # get the nearest neighbors
            distances, neighbors_indexes = self.find_knn(cf_target_sample, target_features_test)

            # asure that the array contains on index nearest neighbors indexes
            customer_index = self.list_index.index(test_index)
            neighbors_indexes = [i for i in neighbors_indexes[0] if i != customer_index]

            metrics = self.calculate_metrics([neighbors_indexes], test_sample.loc[test_index].values, cf_target_sample)
            self.__handle_metrics(metrics, index)

    def __handle_metrics(self, metrics, index):
        fold = self.__metrics[index - 1]
        fold['recall_score'].append(metrics['recall_score'])
        fold['accuracy_score'].append(metrics['accuracy_score'])
        fold['precision_score'].append(metrics['precision_score'])
        fold['f1_score'].append(metrics['f1_score'])

        fold['mean_absolute_error'].append(metrics['mean_absolute_error'])
        fold['mean_squared_error'].append(metrics['mean_squared_error'])
        fold['median_absolute_error'].append(metrics['median_absolute_error'])
        fold['explained_variance_score'].append(metrics['explained_variance_score'])

    def __dump_metrics(self, metrics, best_fold_index):
        logger.info('\n-------******* METRICS -------*******')
        for i in xrange(len(self.__metrics)):
            metrics = self.__metrics[i]
            if i == best_fold_index:
                logger.info('\n**BEST FOLD METRICS ' + str(i) + ' **')
            else:
                logger.info('\n**FOLD ' + str(i) + ' METRICS **')
            for key in metrics.keys():
                avg_value = np.mean(metrics[key])
                std_value = np.std(metrics[key])

                logger.info(key + ' mean = ' + str(avg_value) + ' standard deviation = ' + str(std_value))

    def predict_based_upon_neighbors(self, indexes, cf_matrix):
        items_votes = {}

        # generate the items array with zero ratings
        for item in self.cf_matrix.columns:
            items_votes[item] = 0

        # for each neighbor in neighborhood, sum the items ratings that appears in the neighbor item sample (those who was rated by a neighbor)
        for i in indexes[0]:
            item_ratings = self.cf_matrix.iloc[i]

            for item_key in item_ratings.index:
                items_votes[item_key] += item_ratings[item_key]

        # return self.vote(items_votes, len(self.data.columns))
        votes = []
        for i in items_votes.values():
            if i > 0:
                votes.append(1)
            else:
                votes.append(0)

        return np.array(votes, dtype=int)
        # return items_votes.values()

    def calculate_metrics(self, indexes, expected_ratings, cf_matrix):
        metrics = {}
        # get most voted items
        predicted_ratings = self.predict_based_upon_neighbors(indexes, cf_matrix)

        recall, accuracy, precision, f1 = calculate_classification_metrics(expected_ratings, predicted_ratings)
        metrics['recall_score'] = recall
        metrics['accuracy_score'] = accuracy
        metrics['precision_score'] = precision
        metrics['f1_score'] = f1

        mae, mse, median_ae, evs = calculate_regression_metrics(expected_ratings, predicted_ratings)
        metrics['mean_absolute_error'] = mae
        metrics['mean_squared_error'] = mse
        metrics['median_absolute_error'] = median_ae
        metrics['explained_variance_score'] = evs

        return metrics

    def get_metrics(self):
        return self.__metrics

    def find_knn(self, target_matrix, target_features):
        neighbors = NearestNeighbors(n_neighbors=self.__args.n_neighbors, algorithm=self.__args.alg).fit(
            target_matrix.values)
        distances, indexes = neighbors.kneighbors(target_features)
        return distances, indexes
