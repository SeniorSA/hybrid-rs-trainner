import argparse

from recommender_systems.collaborative_filtering import  UserItemCollaborativeFiltering

parser = argparse.ArgumentParser(description='Recommender Systems trainner')

parser.add_argument('--kfold', help='the number o fold to stratify using k-fold cross-validation', type=float, default=10)
parser.add_argument('--distance-metric', help='the distance metric used to identify nearby items and customers. '
                                              'The metrics available to real-dimensional feature spaces are : \n'
                                              'euclidean \n'
                                              'manhattan \n'
                                              'hebyshev \n'
                                              'minkowski \n'
                                              'wminkowski \n'
                                              'seuclidean \n'
                                              'mahalanobis \n'
                                              'METRICS INTENED FOR BOOLEAN-VALUED VECTOR SPACES AVAILABLE : --- \n'
                                              'jaccard \n'
                                              'matching \n'
                                              'dice \n'
                                              'kulsinski \n'
                                              'rogerstanimoto \n'
                                              'russellrao \n'
                                              'sokalmichener \n'
                                              'sokalsneath \n'
                                              'Metrics intended for two-dimensional vector spaces : -- \n'
                                              'haversine \n'
                                              '-- metrics intented for integers-valued vector spaces: --- \n'
                                              'hamming \n'
                                              'canberra \n'
                                              'braycurtis \n',
                    type=str, default='euclidean')
parser.add_argument('--alg', help='The KNN implementation algorithm. There are four options to chose:\n'
                                  'ball_tree - will use the BallTree\n'
                                  'kd_tree - will use KDTree\n'
                                  'brute - will use a brute-force search.\n'
                                  'auto - will attempt to decide the most appropriate algorithm based on the values passed to fit method',
                    default='brute', type=str)
parser.add_argument('--n-neighbor', help='define the n nearest neighbors', type=int, default=5)
parser.add_argument('--p', default=2, type=int,
                    help='Power parameter for the Minkowski metric. When p = 1, this is equivalent to using manhattan_distance (l1), and euclidean_distance (l2) for p = 2. For arbitrary p, minkowski_distance (l_p) is used.')
parser.add_argument('--leaf-size', type=int, default=30,
                    help='Leaf size passed to BallTree or KDTree. This can affect the speed of the construction and query, as well as the memory required to store the tree. The optimal value depends on the nature of the problem.')
parser.add_argument('--weights', type=str, default='uniform',
                    help='weight function used in prediction. '
                         'Possible values: "uniform" : uniform weights. '
                         'All points in each neighborhood are weighted equally. '
                         '"distance" : weight points by the inverse of their distance. in this case, closer neighbors of a query point will have a greater influence than neighbors which are further away.'
                         '[callable] : a user-defined function which accepts an array of distances, and returns an array of the same shape containing the weights.')

parser.add_argument('--mongo-database-url', help='mongo database url', default='localhost')
parser.add_argument('--mongo-database-name', help='mongo database name', default='testando')
parser.add_argument('--customer-collection-name', help='mongo customer collection name', default='clientes')
parser.add_argument('--item-collection-name', help='mongo item collection name', default='produtos')
parser.add_argument('--billing-collection-name', help='mongo billing collection name', default='faturamento')

args = parser.parse_args()


##inject the data inside
user_item_cbf  = UserItemCollaborativeFiltering(args)
user_item_cbf.train()