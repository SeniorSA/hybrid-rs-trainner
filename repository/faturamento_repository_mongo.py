from repository.faturamento_repository import FaturamentoRepository
from repository.mongo_repository import GenericMongoRepository


class FaturamentoRepositoryMongo(FaturamentoRepository, GenericMongoRepository):
    def __init__(self, repository, collection_name):
        # inject the collection name
        self.repository = repository
        self.repository.collection_name = collection_name
