import argparse
from sklearn.externals import joblib

from repository.cliente_repository_mongo import ClienteRepositoryMongo
from repository.produto_repository_mongo import ProdutoRepositoryMongo, ProdutoRepository
from repository.faturamento_repository_mongo import FaturamentoRepositoryMongo
from repository.mongo_production_repository import MongoProductionRepository
from repository.mongo_repository import GenericMongoRepository
from mongo_utils import load_data

parser = argparse.ArgumentParser(description='Calculate eSocial Campaigns')

parser.add_argument('--pickle-filename', help='specify the pickled filename relative to "classify_data.py"', type=str)
parser.add_argument('--mongo-database-url', help='mongo database url', default='localhost')
parser.add_argument('--mongo-database-name', help='mongo database name', default='testando')
parser.add_argument('--customer-collection-name', help='mongo customer collection name', default='clientes')
parser.add_argument('--item-collection-name', help='mongo item collection name', default='produtos')
parser.add_argument('--billing-collection-name', help='mongo billing collection name', default='faturamentos')
parser.add_argument('--opportunity-collection-name', help='mongo opportunity collection name', default='oportunidades')

args = parser.parse_args()

def load_data():
    item_repository = ProdutoRepositoryMongo(MongoProductionRepository(args), args.item_collection_name)
    billing_repository = FaturamentoRepositoryMongo(MongoProductionRepository(args), args.billing_collection_name)
    customer_repository = ClienteRepositoryMongo(MongoProductionRepository(args), args.customer_collection_name)

    cf_matrix = load_data(customer_repository, item_repository, billing_repository)

    return cf_matrix


user_user_cf = joblib.load(args.pickle_filename)



# items = user_user_cf.cf_matrix.columns
#
# clientes = [
#     "41",
#     "50",
#     "78",
#     "83",
#     "152",
#     "193",
#     "195",
#     "206",
#     "281",
#     "291",
#     "343",
#     "350",
#     "364",
#     "368",
#     "373",
#     "446",
#     "461",
#     "521",
#     "538",
#     "586",
#     "609",
#     "612",
#     "626",
#     "636",
#     "647",
#     "672",
#     "682",
#     "713",
#     "787",
#     "822",
#     "837",
#     "1066",
#     "1109",
#     "1319",
#     "1340",
#     "1837",
#     "1839",
#     "1847",
#     "1863",
#     "1906",
#     "1947",
#     "1975",
#     "2026",
#     "2030",
#     "2033",
#     "2710",
#     "2815",
#     "2879",
#     "2881",
#     "2906",
#     "2930",
#     "3122",
#     "3127",
#     "3128",
#     "3173",
#     "3188",
#     "3250",
#     "3395",
#     "3444",
#     "3649",
#     "3706",
#     "3798",
#     "3832",
#     "4165",
#     "4196",
#     "4615",
#     "4720",
#     "4842",
#     "5121",
#     "5123",
#     "5193",
#     "5205",
#     "5285",
#     "5469",
#     "5485",
#     "5820",
#     "6017",
#     "6342",
#     "6839",
#     "6930",
#     "7074",
#     "7077",
#     "7227",
#     "7303",
#     "7474",
#     "7692",
#     "7728",
#     "7858",
#     "7971",
#     "8171",
#     "9516",
#     "9761",
#     "9784",
#     "9839",
#     "9880",
#     "10038",
#     "10107",
#     "10154",
#     "10219",
#     "10331",
#     "11059",
#     "11168",
#     "11191",
#     "11271",
#     "11284",
#     "11306",
#     "11338",
#     "11489",
#     "11500",
#     "11568",
#     "11595",
#     "11599",
#     "11777",
#     "11862",
#     "11937",
#     "11967",
#     "12008",
#     "12026",
#     "12070",
#     "12228",
#     "12328",
#     "12374",
#     "12423",
#     "12556",
#     "12579",
#     "12581",
#     "12604",
#     "12896",
#     "12910",
#     "13075",
#     "13217",
#     "13243",
#     "13251",
#     "13353",
#     "13527",
#     "13618",
#     "13682",
#     "13710",
#     "13772",
#     "13799",
#     "13909",
#     "13954",
#     "14069",
#     "14102",
#     "14305",
#     "14312",
#     "14358",
#     "14386",
#     "14425",
#     "14513",
#     "14514",
#     "14576",
#     "14590",
#     "14613",
#     "14649",
#     "14659",
#     "14726",
#     "14848",
#     "14958",
#     "14990",
#     "15020",
#     "15059",
#     "15077",
#     "15092",
#     "15114",
#     "15254",
#     "15278",
#     "15418",
#     "15427",
#     "15435",
#     "15524",
#     "15570",
#     "15638",
#     "15948",
#     "16011",
#     "16046",
#     "16102",
#     "16138",
#     "16175",
#     "16227",
#     "16425",
#     "16452",
#     "16602",
#     "16642",
#     "16698",
#     "16724",
#     "16735",
#     "16891",
#     "16913",
#     "16925",
#     "16985",
#     "16998",
#     "17054",
#     "17065",
#     "17079",
#     "17144",
#     "17157",
#     "17182",
#     "17246",
#     "17283",
#     "17293",
#     "17338",
#     "17390",
#     "17444",
#     "17520",
#     "17583",
#     "17636",
#     "17682",
#     "17685",
#     "17712",
#     "17715",
#     "17812",
#     "17848",
#     "17875",
#     "17969",
#     "18101",
#     "18135",
#     "18200",
#     "18202",
#     "18221",
#     "18301",
#     "18327",
#     "18373",
#     "18470",
#     "18615",
#     "18788",
#     "18875",
#     "18892",
#     "18952",
#     "19023",
#     "19129",
#     "19194",
#     "19229",
#     "19413",
#     "19479",
#     "19952"
# ]
#
# import matplotlib.pyplot as plt
#
# from pymongo import MongoClient
#
# db = MongoClient()['testando']
# rows = user_user_cf.cf_matrix.index[:]
# items = user_user_cf.cf_matrix.columns
#
# ratings = user_user_cf.cf_matrix[:]['S-1-100201']
# for i in ratings:
#     if i > 0:
#         print 'i > 0'
#
# ratings = user_user_cf.cf_matrix[:]['S-1-090235']
# for i in ratings:
#     if i > 0:
#         print 'i > 0'  #
#
# # for cliente in clientes:
# #     if cliente not in rows:
# #         clientes.remove(cliente)
# #
# # features = {}
# # for i in items:
# #     features[i] = 0
# #
#
# count = 0
# for cliente in clientes:
#     if cliente in rows:
#         target = user_user_cf.cf_matrix.loc[cliente].values
#         predictions = user_user_cf.predict(target)
#
#         for i in xrange(len(predictions)):
#             recommendation = {'buy': target[i], 'codigoProduto': items[i], 'codigoCliente': cliente}
#             db.knnPredictions.save(recommendation)
#
#     else:
#         count += 1
#
# print count