from skopt import BayesSearchCV
#import time

def hyper_tuning(pso, x_train, y_train):
    space = {"c1":(1, 4),
             "c2":(1, 4),
             "c3":(1, 4),
             "c4":(1, 4)}

    opt = BayesSearchCV(pso, space, n_iter=50, cv=5)
    #t1 = time.time()
    opt.fit(x_train, y_train)
    #t2 = time.time()

    #opt_time = t2 - t1

    #print("val. score: %s" % opt.best_score_)
    #print("test score: %s" % opt.score(validation_data[features], validation_data["safe_loans"]))

    best_tuning = opt.best_params_
    c1 = best_tuning['c1']
    c2 = best_tuning['c2']
    c3 = best_tuning['c3']
    c4 = best_tuning['c4']
    #print("Mejores parámetros:", opt.best_params_

    return c1, c2, c3, c4