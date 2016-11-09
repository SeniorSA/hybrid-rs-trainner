import pandas as pd
import numpy as np
from datetime import datetime
from recommender_systems.collaborative_filtering.user_user_cf import logger


def init_cf_matrix(customer_repository, item_repository):
    customers = np.array(customer_repository.get_customers_code())
    items = np.array(item_repository.get_items_code())
    items_count = len(items)

    cf_matrix = pd.DataFrame(data=0 * items_count, index=customers, columns=items, dtype=int)

    return cf_matrix


def load_data(customer_repository, item_repository, billing_repository, use_date_threshold=True):
    data = datetime(2014, 07, 24)
    count = billing_repository.count()
    documents = None

    if use_date_threshold is True:
        documents = billing_repository.find(0, count, {'data': {'$lt': data}})

    else:
        documents = billing_repository.find()

    logger.info('*INITIALIZING CF MATRIX*')
    cf_matrix = init_cf_matrix(customer_repository=customer_repository, item_repository=item_repository)
    logger.info('*CF MATRIX INITIALIZING COMPLETED* \*LOADING BILLINGS DATA*')

    for target_document in documents:
        rating = round(target_document.get('valorLiquido'))
        customer_code = target_document.get('cliente').get('codigo')
        item_code = target_document.get('produto').get('codigo')

        if item_code in cf_matrix.loc[customer_code].index:
            cf_matrix.loc[customer_code][item_code] += int(rating)

            if cf_matrix.loc[customer_code][item_code] > 0:
                cf_matrix.loc[customer_code][item_code] = 1

            else:
                cf_matrix.loc[customer_code][item_code] = 0

    logger.info('*CF MATRIX INITIALIZING AND COMPUTE RATING COMPLETED*')
    return cf_matrix
