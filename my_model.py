#!/usr/bin/python

import os

from load_data import load_data

from sklearn.ensemble import RandomForestRegressor

from sklearn import cross_validation

def score_model(model, xtrain, ytrain):
    randint = reduce(lambda x,y: x|y, [ord(x)<<(n*8) for (n,x) in enumerate(os.urandom(4))])
    xTrain, xTest, yTrain, yTest = cross_validation.train_test_split(xtrain,
                                                                     ytrain,
                                                                     test_size=0.4, random_state=randint)
    model.fit(xTrain, yTrain)
    print model.score(xTest, yTest)
    #cvAccuracy = np.mean(cross_val_score(model, xtrain, ytrain, cv=2))
    #ytest_pred = model.predict(xTest)
    #print 'rmsle', calculate_rmsle(ytest_pred, yTest)

if __name__ == '__main__':
    xtrain, ytrain, xtest, ytest = load_data()

    model = RandomForestRegressor(n_estimators=400, n_jobs=-1, verbose=1)
    
    score_model(model, xtrain, ytrain)
