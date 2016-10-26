import pickle
from pymongo import MongoClient
from os.path import join, dirname
from sklearn.neighbors import NearestNeighbors
client = MongoClient()
db = client.testando


def load_products_data(skip = 0, top = 0):
    count = db.produtos.count()
    cursor = None
    if top != 0:
        cursor = db.produtos.find().skip(skip * count).limit(top * count)
    else:
        cursor = db.produtos.find()
    atributos_produtos = []
    produtos = []

    for document in cursor:
        linha_de_produto = document.get('linhaDeProduto')
        codigo_linha_produto = '4'
        codigo_familia_produto = '1-MANUT'

        if (linha_de_produto):
            codigo_linha_produto = hash(linha_de_produto.get('codigo'))

        familia = document.get('familia')
        if (familia):
            codigo_familia_produto = hash(familia.get('codigo'))

        produtos.append(document)
        atributos_produtos.append([codigo_linha_produto, codigo_familia_produto])

    return produtos, atributos_produtos

def fit(atributos):
    neighbor = NearestNeighbors(metric='euclidean')
    neighbor.fit(atributos)
    return neighbor

def count_predictions(prediction):
    print(prediction.get('codigo'))
    matches = db.faturamento.find({'produto.codigo': prediction.get('codigo')})

    for match in matches:
        db.recomendacoesScikit.save(match)


def make_predictions(produtos, neighbor):
    for i in xrange(len(produtos)):
        produto = produtos[i]
        linha_de_produto_codigo = '4'
        familia_codigo = '1-MANUT'

        if produto.get('linhaDeProduto'):
            linha_de_produto_codigo = produto.get('linhaDeProduto').get('codigo')

        if produto.get('familia'):
            familia_codigo = produto.get('familia').get('codigo')

        distances, indexes = neighbor.kneighbors([[hash(linha_de_produto_codigo), hash(familia_codigo)]], n_neighbors=15)

        for index in xrange(len(indexes[0])):
            prediction = produtos[index]
            #count_predictions(prediction)
            db.recomendacoesScikit.save({'produtoCodigo': prediction})


def run():
    produtos, atributos = load_products_data()
    neighbor = fit(atributos)
    make_predictions(produtos,neighbor)

run()
