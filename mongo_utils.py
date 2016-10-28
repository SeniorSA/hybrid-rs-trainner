from repository.mongo_production_repository import MongoProductionRepository

def load_data():
    client = MongoProductionRepository()
    data_source = client.get_data_source()

    ##theres an issue hereeee ###