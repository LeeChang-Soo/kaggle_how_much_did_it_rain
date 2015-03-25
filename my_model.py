#!/usr/bin/python

import os
import gzip

import cPickle as pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.cross_validation import train_test_split

from load_data import load_data

def score_model_parallel(model, xtrain, ytrain, yvalue=0):
    randint = reduce(lambda x,y: x|y, [ord(x)<<(n*8) for (n,x) in enumerate(os.urandom(4))])
    xTrain, xTest, yTrain, yTest = train_test_split(xtrain, (ytrain <= yvalue).astype(int),
                                                    test_size=0.4,
                                                    random_state=randint)
    model.fit(xTrain, yTrain)
    print model.score(xTest, yTest)
    
    with gzip.open('model_%d.pkl.gz' % yvalue, 'wb') as mfile:
        pickle.dump(model, mfile, protocol=2)

def create_submission(xtest, ytest, yvalue=0):
    model = None
    with gzip.open('model_%d.pkl.gz' % yvalue, 'rb') as mfile:
        model = pickle.load(mfile)
    
    ypred = model.predict(xtest)
    print ypred

if __name__ == '__main__':
    xtrain, ytrain, xtest, ytest = load_data()

    model = RandomForestClassifier(n_estimators=10, n_jobs=-1, verbose=1)
    #model = RandomForestRegressor(n_estimators=10, n_jobs=-1, verbose=1)
    #model = GradientBoostingRegressor(loss='lad', verbose=1)
    
    score_model_parallel(model, xtrain, ytrain, yvalue=10)
    #create_submission(xtest, ytest)
