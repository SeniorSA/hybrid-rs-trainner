import pandas as pd
import numpy as np


def init_cf_matrix(customer_repository, item_repository):
    customers = np.array(customer_repository.get_customers_code())
    items = np.array(item_repository.get_items_code())
    items_count = len(items)

    cf_matrix = pd.DataFrame(data=0 * items_count, index=customers, columns=items, dtype=int)

    return cf_matrix


def load_data(customer_repository, item_repository, billing_repository):
    documents = billing_repository.find()
    cf_matrix = init_cf_matrix(customer_repository=customer_repository, item_repository=item_repository)

    for target_document in documents:
        rating = target_document.get('valorLiquido')
        customer_code = target_document.get('cliente').get('codigo')
        item_code = hash(target_document.get('produto').get('codigo'))

        if item_code in cf_matrix.columns:
            cf_matrix.loc[customer_code][item_code] += int(rating)

    return cf_matrix
