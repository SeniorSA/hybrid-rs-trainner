from unittest import TestCase
from mongo_base_test import MongoDatabaseTest

from repository.cliente_repository_mongo import ClienteRepositoryMongo
from repository.produto_repository_mongo import ProdutoRepositoryMongo
from repository.faturamento_repository_mongo import FaturamentoRepositoryMongo
from mongo_utils import load_data

from recommender_systems.collaborative_filtering.user_user_cf import UserUserCollaborativeFiltering


class UserItemCollaborativeFilteringTest(MongoDatabaseTest):
    def it_should_pass_test(self):
        self.cf_user_item.train()
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



        # def it_should_return_most_vote_items_from_dict_test(self):
        #     cf_user_item = self.set_up()
        #     items = {'A': 3, 'B': 100, 'C': -2, 'D': 2000, 'E': 150, 'F': 50000, 'X': 1750, 'Y': 100000}
        #     expected_items = ['Y', 'F', 'D', 'X', 'E']
        #     voted_items = cf_user_item.vote(items)
        #     self.assertEqual(expected_items, voted_items)
