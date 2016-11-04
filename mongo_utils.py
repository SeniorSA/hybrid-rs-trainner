from repository.mongo_production_repository import MongoProductionRepository
from repository.faturamento_repository import FaturamentoRepository
from repository.cliente_repository import  ClienteRepository
from repository.produto_repository import ProdutoRepository
from repository.generic_repository import GenericRepository
import pandas as pd
import numpy as np

def init_cf_matrix(args):
    customer_repository = ClienteRepository(MongoProductionRepository(args=args))
    customers = np.array(customer_repository.get_customers_code())

    item_repository = ProdutoRepository(MongoProductionRepository(args=args))
    items = np.array(item_repository.get_items_code())
    items_count = len(items)

    cf_matrix = pd.DataFrame(data=0 * items_count, index=customers, columns=items, dtype=float)

    return cf_matrix


def load_data(args):
    billings = FaturamentoRepository(MongoProductionRepository(args))
    documents = billings.find()
    cf_matrix = init_cf_matrix()

    for target_document in documents:
        rating = target_document.get('valorLiquido')
        customer_code = target_document.get('cliente').get('codigo')
        item_code = target_document.get('produto').get('codigo')
        cf_matrix.loc[customer_code][item_code] += rating

    return cf_matrix