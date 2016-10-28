from generic_repository import GenericRepository

class GenericMongoRepository(GenericRepository):

    def __init__(self, repository):
        self.repository = repository

    def count(self):
        db = self.repository.get_data_source()[self.repository.args.customer_collection_name]
        return db.count()

    def find(self, skip, top):
        data_source = self.repository.get_data_source()
        customer_colls = data_source[self.repository.args.customer_collection_name]
        customers = customer_colls.find()

        if skip != None:
            customers.skip(skip)

        if top != None:
            customers.limit(top)

        return customers
