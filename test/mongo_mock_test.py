from base_test import MongoDatabaseTest
from repository.customer_repository_mongo import CustomerRepositoryMongo

class MongoMockTest(MongoDatabaseTest):

    def it_should_return_19_distincts_customers_test(self):
        repository = CustomerRepositoryMongo(self.mock)
        customers = repository.get_customers_code()
        count = 0
        for i in customers:
            count += 1

        self.assertEqual(count, 19)

    def it_should_return_19_customers_test(self):
        repository = CustomerRepositoryMongo(self.mock)
        count = repository.count()

        self.assertEqual(count, 19)
