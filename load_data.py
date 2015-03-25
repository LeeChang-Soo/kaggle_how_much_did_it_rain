#!/usr/bin/python

import os
import gzip

import matplotlib
matplotlib.use('Agg')
import pylab as pl

import numpy as np
import pandas as pd

def create_html_page_of_plots(list_of_plots, prefix='html'):
    if not os.path.exists(prefix):
        os.makedirs(prefix)
    os.system('mv *.png html')
    #print(list_of_plots)
    idx = 0
    htmlfile = open('%s/index_0.html' % prefix, 'w')
    htmlfile.write('<!DOCTYPE html><html><body><div>\n')
    for plot in list_of_plots:
        if idx > 0 and idx % 200 == 0:
            htmlfile.write('</div></html></html>\n')
            htmlfile.close()
            htmlfile = open('%s/index_%d.html' % (prefix, (idx//200)), 'w')
            htmlfile.write('<!DOCTYPE html><html><body><div>\n')
        htmlfile.write('<p><img src="%s"></p>\n' % plot)
        idx += 1
    htmlfile.write('</div></html></html>\n')
    htmlfile.close()

BINMAP = {u'Nradar': [0,8,8],
          u'TimeToEnd': [0,60,60],
          u'DistanceToRadar': [0,100,100],
          u'Composite': [-20,60,80],
          u'HybridScan': [-20,80,100],
          u'HydrometeorType': [0,14,14],
          u'RR1': [-10,20,100],
          u'RR2': [-10,30,100],
          u'RR3': [-50,50,100],
          u'RadarQualityIndex': [0,1,100],
          u'Reflectivity': [-40,60,100],
          u'ReflectivityQC': [-20,60,80],
          u'RhoHV': [0,2,100],
          u'Velocity': [-40,40,80],
          u'Zdr': [-8,8,100],
          u'LogWaterVolume': [-18,-2,100],
          u'MassWeightedMean': [0,5,100],
          u'MassWeightedSD': [0,2,100],
          u'Expected': [0,70,70]}

def get_plots(in_df, prefix='html'):
    list_of_plots = []

    for c in in_df.columns:
        if c in ['Id',]:
            continue
        pl.clf()
        v = in_df[c][in_df[c].notnull()]
        nent = len(v)
        if nent == 0:
            continue
        hmin, hmax = v.min(), v.max()
        #xbins = np.linspace(hmin,hmax,nent//500)
        hmin, hmax, nbin = BINMAP[c]
        xbins = np.linspace(hmin,hmax,nbin)

        if 'Expected' in in_df.columns:
            cond0 = in_df['Expected'] == 0.
            cond1 = in_df['Expected'] > 0.
        else:
            cond0 = in_df['RadarQualityIndex'] <= -99
            cond1 = in_df['RadarQualityIndex'] > -99

        a = v[cond0].values
        pl.hist(a, bins=xbins, histtype='step', log=False)
        pl.title(c)

        b = v[cond1].values
        pl.hist(b, bins=xbins, histtype='step', log=False)

        pl.savefig('%s.png' % c)
        list_of_plots.append('%s.png' % c)
    create_html_page_of_plots(list_of_plots, prefix=prefix)

def clean_data(indf):
    print 'call clean data'

    for c in ['RadarQualityIndex', 'Composite', 'HybridScan', 'RR1', 'RR2',
              'RR3', 'Reflectivity', 'ReflectivityQC', 'RhoHV', 'Velocity',
              'Zdr', 'LogWaterVolume', 'MassWeightedMean', 'MassWeightedSD']:
        indf.loc[indf[c].isnull(), c] = -100

    indf = indf.drop(labels=['Kdp'], axis=1)
    return indf

def load_data():
    train_df = pd.read_csv('train_2013_full.csv.gz', compression='gzip')
    test_df = pd.read_csv('test_2014_full.csv.gz', compression='gzip')
    submit_df = pd.read_csv('sampleSubmission.csv.gz', compression='gzip')

    train_df = clean_data(train_df)
    test_df = clean_data(test_df)

    print train_df.columns

    get_plots(train_df, prefix='html_train')
    get_plots(test_df, prefix='html_test')

    print train_df.shape

    xtrain = train_df.drop(labels=['Id', 'Expected'], axis=1).values
    ytrain = train_df['Expected'].values
    xtest = test_df.drop(labels=['Id',], axis=1).values
    ytest = submit_df

    print xtrain.shape, ytrain.shape, xtest.shape, ytest.shape

    return xtrain, ytrain, xtest, ytest

if __name__ == '__main__':
    xtrain, ytrain, xtest, ytest = load_data()
