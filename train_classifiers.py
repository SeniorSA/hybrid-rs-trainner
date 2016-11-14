import argparse
from sklearn.externals import joblib
from recommender_systems.collaborative_filtering import UserUserCollaborativeFiltering

from repository.cliente_repository import ClienteRepositoryMongo
from repository.produto_repository import ProdutoRepositoryMongo, ProdutoRepository
from repository.faturamento_repository import FaturamentoRepositoryMongo
from repository.mongo_production_repository import MongoProductionRepository
from repository.mongo_repository import GenericMongoRepository
from mongo_utils import load_data
from recommender_systems.collaborative_filtering.user_user_cf import logger, file_name
from train_recommender import  args


item_repository = ProdutoRepositoryMongo(MongoProductionRepository(args), args.item_collection_name)
billing_repository = FaturamentoRepositoryMongo(MongoProductionRepository(args), args.billing_collection_name)
customer_repository = ClienteRepositoryMongo(MongoProductionRepository(args), args.customer_collection_name)

cf_matrix = load_data(customer_repository, item_repository, billing_repository)

user_user_cf = UserUserCollaborativeFiltering(args, cf_matrix)
user_user_cf.train()

logger.info('---STARTING MODEL PERSISTENCE---')
joblib.dump(user_user_cf, file_name + '.pkl')
logger.info('---FINISHED MODEL PERSISTENCE--')
