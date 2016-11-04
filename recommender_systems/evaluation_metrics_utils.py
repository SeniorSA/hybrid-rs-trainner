from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error, explained_variance_score, \
    accuracy_score, f1_score, precision_score, recall_score


def calculate_classification_metrics(expected, predicted):
    recall = recall_score(expected, predicted)
    accuracy = accuracy_score(expected, predicted)
    precision = precision_score(expected, predicted)
    f1 = f1_score(expected, predicted)

    return recall, accuracy, precision, f1


def calculate_regression_metrics(expected, predicted):
    mae = mean_absolute_error(expected, predicted)
    mse = mean_squared_error(expected, predicted)
    median_ae = median_absolute_error(expected, predicted)
    evs = explained_variance_score(expected, predicted)

    return mae, mse, median_ae, evs
