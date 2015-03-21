#!/usr/bin/python

import os
import gzip

import matplotlib
matplotlib.use('Agg')
import pylab as pl

import numpy as np
import pandas as pd

def create_html_page_of_plots(list_of_plots):
    if not os.path.exists('html'):
        os.makedirs('html')
    os.system('mv *.png html')
    #print(list_of_plots)
    idx = 0
    htmlfile = open('html/index_0.html', 'w')
    htmlfile.write('<!DOCTYPE html><html><body><div>\n')
    for plot in list_of_plots:
        if idx > 0 and idx % 200 == 0:
            htmlfile.write('</div></html></html>\n')
            htmlfile.close()
            htmlfile = open('html/index_%d.html' % (idx//200), 'w')
            htmlfile.write('<!DOCTYPE html><html><body><div>\n')
        htmlfile.write('<p><img src="%s"></p>\n' % plot)
        idx += 1
    htmlfile.write('</div></html></html>\n')
    htmlfile.close()

def get_plots(in_df):
    list_of_plots = []
    #print in_df.columns

    for c in in_df.columns:
        if c in ['Id',]:
            continue
        pl.clf()
        v = in_df[c][in_df[c].notnull()]
        nent = len(v)
        hmin, hmax = v.min(), v.max()
        xbins = np.linspace(hmin,hmax,nent)
        a = v.values
        try:
            pl.hist(a, bins=xbins, histtype='step', log=False)
        except ValueError:
            print xbins, hmin, hmax, nent, v.dtype
            print np.isnan(hmin), np.isnan(hmax)
            exit(0)
        except IndexError:
            print xbins, hmin, hmax, nent, v.dtype
            print np.isnan(hmin), np.isnan(hmax)
            exit(0)
        pl.title(c)
        pl.savefig('%s.png' % c)
        list_of_plots.append('%s.png' % c)
    create_html_page_of_plots(list_of_plots)

def clean_data(indf):
    print 'call clean data'
    
    return indf

def load_data(is_test=False):
    fname = 'train_2013_avg.csv.gz'
    if is_test:
        fname = 'test_2014_avg.csv.gz'

    df = pd.read_csv(fname, compression='gzip')
    
    df = clean_data(df)
    
    print df.columns
    
    #get_plots(df)

    print df['HydrometeorType']
    
    return

if __name__ == '__main__':
    load_data()
