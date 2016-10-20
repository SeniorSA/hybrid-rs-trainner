from pymongo import MongoClient
from os.path import join, dirname
from sklearn.neighbors import NearestNeighbors

def load_products_data():
    client = MongoClient()
    db = client.testando
    cursor = db.produtos.find().limit(100)
    atributos_produtos = []
    codigos_produtos = []

    for document in cursor:
        linha_de_produto = document.get('linhaDeProduto')
        codigo_linha_produto = '0'
        codigo_familia_produto = '0'

        if (linha_de_produto):
            codigo_linha_produto = hash(linha_de_produto.get('codigo'))

        familia = document.get('familia')
        if (familia):
            codigo_familia_produto = hash(familia.get('codigo'))

        codigos_produtos.append(document.get('codigo'))
        atributos_produtos.append([codigo_linha_produto, codigo_familia_produto])

    return codigos_produtos, atributos_produtos


produtos, atributos = load_products_data()
neighbor = NearestNeighbors(metric='euclidean')
neighbor.fit(atributos)
distances, indexes = neighbor.kneighbors([[hash('8'), hash('100-GCS')]], n_neighbors=5)

for index in indexes:
    for j in index:
        print(produtos[j])



def load_customers_data():
    client = MongoClient()
    db = client.testando
    cursor = db.clientes.find().limit(100)

    atributos_clientes = []
    clientes = []

    for document in cursor:
        ramo_codigo = '0'
        porte_codigo = '0'


        latitude_cidade = '0'
        longitude_cidade = '0'

        latitude_estado = '0'
        longitude_estado = '0'

        ramo = document.get('ramoDeAtividade')
        if (ramo):
            ramo_codigo = ramo.get('codigo')

        porte = document.get('porte')
        if (porte):
            porte_codigo = porte.get('codigo')


        cliente_codigo = document.get('codigo')

        cidade = document.get('cidade')

        if (cidade):
            latitude_cidade = cidade.get('latitude')
            longitude_cidade = cidade.get('longitude')

            if (cidade.get('estado')):
                latitude_estado = cidade.get('estado').get('latitude')
                longitude_estado = cidade.get('estado').get('longitude')


        atributos_clientes.append([porte_codigo, ramo_codigo, latitude_estado, longitude_estado, latitude_cidade, longitude_cidade])
        clientes.append(cliente_codigo)

    return clientes, atributos_clientes

# clientes, atributos = load_customers_data()
#
# neighbor = NearestNeighbors(metric='euclidean')
# neighbor.fit(atributos)
# a, b = neighbor.kneighbors([[2, 501]], n_neighbors=2)
