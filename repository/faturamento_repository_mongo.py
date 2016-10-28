from repository.faturamento_repository import FaturamentoRepository
from repository.mongo_repository import GenericMongoRepository


class FaturamentoRepositoryMongo(FaturamentoRepository, GenericMongoRepository):
    def __init__(self, repository):
        self.repository = repository
