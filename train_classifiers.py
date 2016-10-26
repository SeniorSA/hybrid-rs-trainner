import argparse


parser = argparse.ArgumentParser(description='Recommender Systems trainner')

parser.add_argument('--kfold', help='the number o fold to stratify using k-fold cross-validation', type=int, default=0)
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

args = parser.parse_args()

print(args.kfold)
print(args.distance_metric)