from generic_repository import GenericRepository

class GenericMongoRepository(GenericRepository):

    def __init__(self, repository):
        self.repository = repository

    def __get_repository_name(self):
        class_n = self.__class__.__name__.split('Repository')[0].lower()
        return class_n + 's'

    def count(self):
        db = self.repository.get_data_source()[self.__get_repository_name()]
        return db.count()

    def find(self, skip = 0, top=50000000):
        data_source = self.repository.get_data_source()
        customer_colls = data_source[self.__get_repository_name()]
        customers = customer_colls.find()

        if skip != None:
            customers.skip(skip)

        if top != None:
            customers.limit(top)

        return customers
