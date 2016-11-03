from repository.mongo_production_repository import MongoProductionRepository
import pandas as pd
import numpy as np

client = MongoProductionRepository()
db = client.get_data_source()


def __init_cf_matrix(self):
    customers = np.array(db.clientes.distinct('codigo'))
    items = np.array(db.produtos.distinct('codigo'))

    items = np.array(self.__items)
    items_count = len(items)

    cf_matrix = pd.DataFrame(data=0 * items_count, index=customers, columns=items, dtype=float)

    return cf_matrix


def fit_cf_matrix(self, documents):
    cf_matrix = self.__init_cf_matrix()

    # veryfied
    for target_document in documents:
        rating = target_document.get('valorLiquido')
        customer_code = target_document.get('cliente').get('codigo')
        item_code = target_document.get('produto').get('codigo')
        cf_matrix.loc[customer_code][item_code] += rating

    return cf_matrix


def __init_cf_matrix(self):
    customers = np.array(self.__customers)
    items = np.array(self.__items)
    items_count = len(items)

    cf_matrix = pd.DataFrame(data=0 * items_count, index=customers, columns=items, dtype=float)

    return cf_matrix