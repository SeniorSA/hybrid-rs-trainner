from repository.billing_repository import BillingRepository
from repository.mongo_repository import GenericMongoRepository


class BillingRepositoryMongo(BillingRepository, GenericMongoRepository):
    def __init__(self, repository):
        self.repository = repository
