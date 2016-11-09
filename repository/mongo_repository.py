from generic_repository import GenericRepository


class GenericMongoRepository(GenericRepository):
    def __init__(self, repository, collection_name):
        self.repository = repository

    def __get_repository_name(self):
        class_n = self.__class__.__name__.split('Repository')[0].lower()
        return class_n + 's'

    def count(self):
        db = self.repository.get_data_source()[self.repository.collection_name]
        return db.count()

    def find(self, skip=0, top=None, query=None):
        if top == None:
            top = self.count()

        data_source = self.repository.get_data_source()
        customer_colls = data_source[self.repository.collection_name]

        documents = None

        if query != None:
            documents = customer_colls.find(query)

        else:
            documents = customer_colls.find()

        if skip != None:
            documents.skip(skip)

        if top != None:
            documents.limit(top)

        return documents
