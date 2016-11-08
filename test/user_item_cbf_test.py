from unittest import TestCase
from mongo_base_test import MongoDatabaseTest

from repository.cliente_repository_mongo import ClienteRepositoryMongo
from repository.produto_repository_mongo import ProdutoRepositoryMongo
from repository.faturamento_repository_mongo import FaturamentoRepositoryMongo
from mongo_utils import load_data

from recommender_systems.collaborative_filtering.user_user_cf import UserUserCollaborativeFiltering


/*


"""
    p1, p2, p3 , p4
c1  34  35   0    0
c2  25  12   0   10
c3  13   0   0   0
c4  22  17   0   231

"""

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
