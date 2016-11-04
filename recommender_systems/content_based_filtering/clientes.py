from pymongo import MongoClient



def load_customers_data():
    client = MongoClient()
    db = client.testando
    cursor = db.clientes.find().limit(10)

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

        atributos_clientes.append(
            [porte_codigo, ramo_codigo, latitude_estado, longitude_estado, latitude_cidade, longitude_cidade])
        clientes.append(cliente_codigo)

    return clientes, atributos_clientes

# clientes, atributos = load_customers_data()
#
# neighbor = NearestNeighbors(metric='euclidean')
# neighbor.fit(atributos)
# a, b = neighbor.kneighbors([[2, 501]], n_neighbors=2)
