#!/usr/bin/python

import os
import gzip

import cPickle as pickle

import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier

from sklearn.grid_search import GridSearchCV

from sklearn.cross_validation import train_test_split

from load_data import load_data

def score_model_parallel(model, xtrain, ytrain, yvalue=0, do_grid_search=False):
    randint = reduce(lambda x,y: x|y, [ord(x)<<(n*8) for (n,x) in enumerate(os.urandom(4))])
    xTrain, xTest, yTrain, yTest = train_test_split(xtrain, (ytrain <= yvalue).astype(int),
                                                    test_size=0.4,
                                                    random_state=randint)
    n_est = [10, 20]
    m_dep = [2, 3, 4, 5, 6, 7, 10]

    if do_grid_search:
        model = GridSearchCV(estimator=model,
                                    param_grid=dict(n_estimators=n_est,
                                                    max_depth=m_dep),
                                    scoring=scorer,
                                    n_jobs=-1, verbose=1)

    model.fit(xTrain, yTrain)
    print model.score(xTest, yTest)

    with gzip.open('model_%d.pkl.gz' % yvalue, 'wb') as mfile:
        pickle.dump(model, mfile, protocol=2)

def create_submission_parallel(xtest, ytest):
    model = None
    for idx in range(0,70):
        with gzip.open('model_%d.pkl.gz' % idx, 'rb') as mfile:
            model = pickle.load(mfile)

        #ypred = model.predict(xtest)
        #print ypred
        yprob = model.predict_proba(xtest)
        print yprob
        ytest['Predicted%d' % idx] = yprob[:,1]

    for idx in range(1,70):
        ytest['Predicted%d' % idx] = np.max(ytest[['Predicted%d' % (idx-1), 'Predicted%d' % idx]], axis=1)

    ytest.to_csv('submission.csv.gz', compression='gzip', index=False)

if __name__ == '__main__':
    xtrain, ytrain, xtest, ytest = load_data()

    begin_idx = -1
    end_idx = -1
    for arg in os.sys.argv:
        try:
            index = int(arg)
            if begin_idx == -1:
                begin_idx = index
            elif end_idx == -1:
                end_idx = index
                break
        except ValueError:
            continue
    if begin_idx == -1:
        begin_idx = 0
    if end_idx == -1:
        end_idx = 69

    print begin_idx, end_idx

    if begin_idx < 70:
        #model = SGDClassifier(loss='log', n_jobs=-1, penalty='l1', verbose=1, n_iter=200)
        model = GradientBoostingClassifier(loss='deviance', verbose=1)
#        model = RandomForestClassifier(n_estimators=10, n_jobs=-1, verbose=1)


        for idx in range(begin_idx, end_idx+1):
            score_model_parallel(model, xtrain, ytrain, yvalue=idx,
                                 do_grid_search=True)
    elif begin_idx == 70:
        create_submission_parallel(xtest, ytest)
