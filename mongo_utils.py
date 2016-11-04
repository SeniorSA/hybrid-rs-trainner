import pandas as pd
import numpy as np


def init_cf_matrix(customer_repository, item_repository):
    customers = np.array(customer_repository.get_customers_code())
    items = np.array(item_repository.get_items_code())
    items_count = len(items)

    cf_matrix = pd.DataFrame(data=0 * items_count, index=customers, columns=items, dtype=float)

    return cf_matrix


def load_data(customer_repository, item_repository, billing_repository):
    documents = billing_repository.find()
    cf_matrix = init_cf_matrix(customer_repository=customer_repository, item_repository=item_repository)

    for target_document in documents:
        rating = target_document.get('valorLiquido')
        if rating > 0:
            rating = 1
        else:
            rating = 0
        customer_code = target_document.get('cliente').get('codigo')
        item_code = target_document.get('produto').get('codigo')
        cf_matrix.loc[customer_code][item_code] += rating

    return cf_matrix
