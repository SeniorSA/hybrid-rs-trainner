from mongo_base_test import MongoDatabaseTest
from repository.cliente_repository_mongo import ClienteRepositoryMongo
from repository.faturamento_repository_mongo import FaturamentoRepositoryMongo
from repository.produto_repository_mongo import ProdutoRepositoryMongo

class MongoMockRepositoryTest(MongoDatabaseTest):

    def it_should_return_19_distincts_customers_test(self):
        repository = ClienteRepositoryMongo(self.repository_mock)
        customers = repository.get_customers_code()
        count = 0
        for i in customers:
            count += 1

        self.assertEqual(count, 14)

    def it_should_return_14_customers_test(self):
        repository = ClienteRepositoryMongo(self.repository_mock)
        count = repository.count()

        self.assertEqual(count, 14)

    def it_should_return_billings_count_which_its_equals_to_200_test(self):
        repository = FaturamentoRepositoryMongo(self.repository_mock)
        count = repository.count()

        self.assertEqual(count, 20)

    def it_should_return_items_count_which_its_equals_to_3_test(self):
        repository = ProdutoRepositoryMongo(self.repository_mock)
        count = repository.count()

        self.assertEqual(count, 3)