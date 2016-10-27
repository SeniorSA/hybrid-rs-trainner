from abc import abstractmethod, ABCMeta
from repository.repository_factory import RepositoryFactory
from repository.customer_repository import CustomerRepository


class CustomerRepositoryMongo(object, CustomerRepository):
    def __init__(self, repository):
        self.repository = repository

    def get_customers_code(self):
        db = self.repository[self.args.mongo_database_name]
        customer_colls = db[self.args.mongo_collection_name]
        customer_codes = customer_colls.distinct('codigo')

        return customer_codes
