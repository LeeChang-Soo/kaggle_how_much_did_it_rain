#!/usr/bin/python

import os
import gzip

import cPickle as pickle

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import train_test_split

from load_data import load_data

def score_model(model, xtrain, ytrain):
    randint = reduce(lambda x,y: x|y, [ord(x)<<(n*8) for (n,x) in enumerate(os.urandom(4))])
    xTrain, xTest, yTrain, yTest = train_test_split(xtrain, ytrain,
                                                    test_size=0.6,
                                                    random_state=randint)
    model.fit(xTrain, yTrain)
    print model.score(xTest, yTest)
    
    with gzip.open('model.pkl.gz' % index, 'wb') as mfile:
        pickle.dump(model, mfile, protocol=2)

if __name__ == '__main__':
    xtrain, ytrain, xtest, ytest = load_data()

    #model = RandomForestRegressor(n_estimators=10, n_jobs=-1, verbose=1)
    model = GradientBoostingRegressor(loss='lad', verbose=1, n_jobs=-1)
    
    score_model(model, xtrain, ytrain)
