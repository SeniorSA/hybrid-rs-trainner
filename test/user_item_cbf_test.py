from unittest import TestCase
from mongo_base_test import MongoDatabaseTest

from repository.cliente_repository_mongo import ClienteRepositoryMongo
from repository.produto_repository_mongo import ProdutoRepositoryMongo
from repository.faturamento_repository_mongo import FaturamentoRepositoryMongo

from recommender_systems.collaborative_filtering.user_item_cbf import UserItemCollaborativeFiltering


class UserItemCollaborativeFilteringTest(MongoDatabaseTest):
    def it_should_pass_test(self):
        produto_repository = ProdutoRepositoryMongo(self.repository_mock)
        items = produto_repository.get_customers_code()

        cliente_repository = ClienteRepositoryMongo(self.repository_mock)
        customers = cliente_repository.get_customers_code()

        faturamento_repostiory = FaturamentoRepositoryMongo(self.repository_mock)
        billings = faturamento_repostiory.find()

        cf_user_item = UserItemCollaborativeFiltering(self.mock_args(), billings, customers, items)

        cf_user_item.train()

        self.assertTrue(True)
