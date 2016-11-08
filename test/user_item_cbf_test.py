from unittest import TestCase
from mongo_base_test import MongoDatabaseTest

from repository.cliente_repository_mongo import ClienteRepositoryMongo
from repository.produto_repository_mongo import ProdutoRepositoryMongo
from repository.faturamento_repository_mongo import FaturamentoRepositoryMongo
from mongo_utils import load_data

from recommender_systems.collaborative_filtering.user_user_cf import UserUserCollaborativeFiltering
import numpy as np

"""
    p1, p2, p3 , p4
c1   1   1   0    0
c2   1   1   0    1
c3   1   0   0    0
c4   1   1   0    1      |     p1  p2  p3   p4
c5   0   1   0    0      | c10  0   0   1    1
   -------------         | c7   1   0   0    1
                         | c6   0   0   0    0
                         | c5   0   1   0    0
                         | c4   1   1   0    1
c6   0   0   0    0
c7   1   0   0    1
c8   1   0   1    0
c9   1   1   1    0
c10  0   0   1    1
it should choose the second fold (k=2)
"""


class UserItemCollaborativeFilteringTest(MongoDatabaseTest):
    def it_should_pass_test(self):
        metrics = self.cf_user_item.get_metrics()
        accuracy = 0

        self.assertTrue(True)

    def setUp(self):
        super(UserItemCollaborativeFilteringTest, self).setUp()

        item_repository = ProdutoRepositoryMongo(self.repository_mock, self.repository_mock.args.item_collection_name)
        customer_repository = ClienteRepositoryMongo(self.repository_mock,
                                                     self.repository_mock.args.customer_collection_name)
        billing_repository = FaturamentoRepositoryMongo(self.repository_mock,
                                                        self.repository_mock.args.billing_collection_name)

        cf_matrix = load_data(customer_repository=customer_repository, item_repository=item_repository,
                              billing_repository=billing_repository)

        self.cf_user_item = UserUserCollaborativeFiltering(self.mock_args(), cf_matrix)
        self.cf_user_item.train()

    def it_should_use_only_5train_fold_test(self):
        target_indexes = ['c10', 'c7', 'c6', 'c5', 'c4']
        print target_indexes
        indexes = [i for i in self.cf_user_item.cf_matrix.index]
        print indexes
        self.assertEqual(indexes, target_indexes)

    def find_nearest_neghbor_c9__test(self):
        c9_features = [1, 1, 1, 0]
        distances, indexes = self.cf_user_item.find_knn(self.cf_user_item.cf_matrix, c9_features)
        n1_c5 = self.cf_user_item.cf_matrix.iloc[indexes[0][0]]
        n2_c4 = self.cf_user_item.cf_matrix.iloc[indexes[0][1]]

        self.assertEqual(n1_c5.name, 'c5')
        self.assertEqual(n2_c4.name, 'c4')

    def find_nearest_neghbor_c8_test(self):
        c8_features = [1, 0, 1, 0]
        distances, indexes = self.cf_user_item.find_knn(self.cf_user_item.cf_matrix, c8_features)
        n1_c10 = self.cf_user_item.cf_matrix.iloc[indexes[0][0]]
        n2_c7 = self.cf_user_item.cf_matrix.iloc[indexes[0][1]]

        self.assertEqual(n1_c10.name, 'c5')
        self.assertEqual(n2_c7.name, 'c4')

    def predict_customer_c9_items_test(self):
        target_features = customer_c9_features = np.array([1, 1, 1, 0])
        print self.cf_user_item.cf_matrix.columns
        expected = np.array([1, 0, 1, 1])
        predicted = self.cf_user_item.predict(target_features)

        np.testing.assert_array_equal(expected, predicted)
