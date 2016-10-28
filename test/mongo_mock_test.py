from base_test import MongoDatabaseTest
from repository.cliente_repository_mongo import ClienteRepositoryMongo
from repository.faturamento_repository_mongo import FaturamentoRepositoryMongo


class MongoMockTest(MongoDatabaseTest):
    def it_should_return_19_distincts_customers_test(self):
        repository = ClienteRepositoryMongo(self.mock)
        customers = repository.get_customers_code()
        count = 0
        for i in customers:
            count += 1

        self.assertEqual(count, 19)

    def it_should_return_19_customers_test(self):
        repository = ClienteRepositoryMongo(self.mock)
        count = repository.count()

        self.assertEqual(count, 19)

    def it_should_return_billings_count_which_its_equals_to_200_test(self):
        repository = FaturamentoRepositoryMongo(self.mock)
        count = repository.count()

        self.assertEqual(count, 200)
