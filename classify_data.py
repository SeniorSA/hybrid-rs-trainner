import argparse
from sklearn.externals import joblib
import numpy as np
import pandas as pd
from pymongo import MongoClient

from repository.cliente_repository import ClienteRepositoryMongo
from repository.produto_repository import ProdutoRepositoryMongo
from repository.faturamento_repository import FaturamentoRepositoryMongo
from repository.oportunidade_repository import OportunidadeRepositoryMongo
from repository.mongo_production_repository import MongoProductionRepository
from repository.mongo_repository import GenericMongoRepository

parser = argparse.ArgumentParser(description='Calculate eSocial Campaigns')

parser.add_argument('--pickle-filename', help='specify the pickled filename relative to "classify_data.py"', type=str,
                    default='user_user_cf_knn-10-11-2016-9-27-0.pkl')
parser.add_argument('--mongo-database-url', help='mongo database url', default='localhost')
parser.add_argument('--mongo-database-name', help='mongo database name', default='testando')
parser.add_argument('--customer-collection-name', help='mongo customer collection name', default='clientes')
parser.add_argument('--item-collection-name', help='mongo item collection name', default='produtos')
parser.add_argument('--billing-collection-name', help='mongo billing collection name', default='faturamentos')
parser.add_argument('--opportunity-collection-name', help='mongo opportunity collection name', default='oportunidades')

args = parser.parse_args()

user_user_cf = joblib.load(args.pickle_filename)

target_items = ['S-1-100201', 'S-1-090235']
db = MongoClient()['testando']

item_repository = ProdutoRepositoryMongo(MongoProductionRepository(args), args.item_collection_name)

columns = item_repository.get_items_code()


def load_data(cf_matrix):
    billing_repository = FaturamentoRepositoryMongo(MongoProductionRepository(args), args.billing_collection_name)
    count = billing_repository.count()

    for customer_code in cf_matrix.index:
        documents = billing_repository.find(0, count, {'cliente.codigo': customer_code})

        for doc in documents:
            item_code = doc.get('produto').get('codigo')
            cf_matrix.loc[customer_code][item_code] = 1


def init_matrix():
    opportunity_repository = OportunidadeRepositoryMongo(MongoProductionRepository(args),
                                                         args.opportunity_collection_name)
    customers = opportunity_repository.get_customers_code()

    data = []

    for customer in customers:
        target_features = [i * 0 for i in xrange(len(columns))]
        data.append(target_features)

    test_matrix = pd.DataFrame(data=data, index=customers, columns=columns, dtype=int)

    load_data(test_matrix)

    return test_matrix


def save_predictions(test_matrix):
    for customer_code in test_matrix.index:
        target_features = test_matrix.loc[customer_code].values
        predictions = user_user_cf.predict(target_features)

        for i in xrange(len(predictions)):
            recommendation = {'buy': predictions[i], 'codigoProduto': columns[i], 'codigoCliente': customer_code,
                              'version': args.pickle_filename}
            db.knnPredictions.save(recommendation)


test_matrix = init_matrix()
save_predictions(test_matrix)
