from skopt import BayesSearchCV
import gpbasedpso
from numpy import mean
from sklearn.datasets import make_blobs
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from skopt.space import Integer
from skopt.utils import use_named_args
from skopt import gp_minimize


model = gpbasedpso
# define the space of hyperparameters to search
hyperparameter = {'c1': [1, 2, 3, 4],
                  'c2': [1, 2, 3, 4],
                  'c3': [1, 2, 3, 4],
                  'c4': [1, 2, 3, 4],
                  'n': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200],
                  'leng_scale': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]}


# define the function used to evaluate a given configuration
@use_named_args(hyperparameter)
def evaluate_model(**params):
    # something
    model.set_params(**params)
    # calculate 5-fold cross validation
    result = cross_val_score(model, X, y, cv=5, n_jobs=-1, scoring='accuracy')
    # calculate the mean of the scores
    estimate = mean(result)
    return 1.0 - estimate


# perform optimization
result = gp_minimize(evaluate_model, search_space)
# summarizing finding:
print('Best Accuracy: %.3f' % (1.0 - result.fun))
print('Best Parameters: n_neighbors=%d, p=%d' % (result.x[0], result.x[1]))


# import time

def hyper_tuning():


    opt = BayesSearchCV(gpbasedpso, hyperparameter, n_iter=50, cv=5)
    # t1 = time.time()
    opt.fit(x_train, y_train)
    # t2 = time.time()

    # opt_time = t2 - t1

    # print("val. score: %s" % opt.best_score_)
    # print("test score: %s" % opt.score(validation_data[features], validation_data["safe_loans"]))

    best_tuning = opt.best_params_
    c1 = best_tuning['c1']
    c2 = best_tuning['c2']
    c3 = best_tuning['c3']
    c4 = best_tuning['c4']
    # print("Mejores parámetros:", opt.best_params_

    return c1, c2, c3, c4
