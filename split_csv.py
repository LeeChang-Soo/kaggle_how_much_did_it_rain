#!/usr/bin/python

import os
import gzip
import csv

import numpy as np

nan_vals = [-99900, -99901, -99903, 999]

def count_decreasing(x):
    numb = 0
    arr = [0]
    prev = x[0]
    for idx in range(1,len(x)):
        if x[idx] > prev:
            numb += 1
        prev = x[idx]
        arr.append(numb)
    return np.array(arr)

def count_distances(x):
    numb = 0
    arr = [0]
    prev = x[0]
    for idx in range(1,len(x)):
        if x[idx] != prev:
            numb += 1
        prev = x[idx]
        arr.append(numb)
    return np.array(arr)

def reduce_subrows(subrows):
    avgrow = {x: 0 for x in subrows.keys()}
    numrow = {x: 1 for x in subrows.keys()}
    avgrow['HydrometeorType'] = 8
    for val in subrows['HydrometeorType']:
        if int(val) not in (0,7,8,9):
            avgrow['HydrometeorType'] = int(val)
    for col in ['HybridScan', 'MassWeightedMean', 'Composite', 'RR3', 'MassWeightedSD', 'Reflectivity', 'RR2', 'RadarQualityIndex', 'ReflectivityQC', 'LogWaterVolume', 'RhoHV', 'Velocity', 'Zdr', 'Kdp', 'HydrometeorType', 'RR1', 'DistanceToRadar', 'TimeToEnd']:
        if np.all(np.isnan(subrows[col])):
            avgrow[col] = np.nan
            numrow[col] = 1
        else:
            cond = np.isfinite(subrows[col])
            avgrow[col] = np.sum(subrows[col][cond], dtype=np.float64)
            numrow[col] = np.sum(cond, dtype=np.float64)
    for col in avgrow.keys():
        avgrow[col] = avgrow[col] / numrow[col]
    return avgrow

def split_csv(is_test=False, number_of_files=1, number_of_events=-1):
    orig_csv_file = 'train_2013.csv.gz'
    output_prefix = 'train_2013_full'
    if is_test:
        orig_csv_file = 'test_2014.csv.gz'
        output_prefix = 'test_2014_full'

    if number_of_files == 1:
        output_files = [gzip.open('%s.csv.gz' % output_prefix, 'w')]
    else:
        output_files = [gzip.open('%s_%d.csv.gz' % (output_prefix, n), 'w') for n in range(10)]
    csv_writers = [csv.writer(f) for f in output_files]

    labels_to_write = ['Id', 'Nradar', 'TimeToEnd', 'DistanceToRadar', 'Composite', 'HybridScan', 'HydrometeorType', 'Kdp', 'RR1', 'RR2', 'RR3', 'RadarQualityIndex', 'Reflectivity', 'ReflectivityQC', 'RhoHV', 'Velocity', 'Zdr', 'LogWaterVolume', 'MassWeightedMean', 'MassWeightedSD']
    if not is_test:
        labels_to_write.append('Expected')

    with gzip.open(orig_csv_file, 'r') as infile:
        csv_reader = csv.reader(infile)
        labels = next(csv_reader)
        for c in csv_writers:
            c.writerow(labels_to_write)
        for idx, row in enumerate(csv_reader):
            if number_of_events > 0 and idx > number_of_events:
                break
            if idx % 100000 == 0:
                print 'processed %d events' % idx
            row_dict = dict(zip(labels, row))

            if 'Expected' in row_dict:
                if float(row_dict['Expected']) > 70.0:
                    row_dict['Expected'] = 70.0

            subrows = {}

            for label in labels_to_write:
                if label in ['Id', 'Expected', 'Nradar']:
                    continue
                for nan_str in ['-99900.0', '-99901.0', '-99903.0', '999.0']:
                    row_dict[label] = row_dict[label].replace(nan_str, 'nan')
                subrows[label] = np.fromstring(row_dict[label], sep=' ')

            time_idx = count_decreasing(subrows['TimeToEnd'])
            dist_idx = count_distances(subrows['DistanceToRadar'])

            max_idx = np.max([time_idx, dist_idx], axis=0)

            row_dict['Nradar'] = max_idx[-1]+1

            subrows = reduce_subrows(subrows)

            for label in labels_to_write:
                if label not in ['Id', 'Nradar', 'Expected']:
                    row_dict[label] = subrows[label]
            row_val = [row_dict[col] for col in labels_to_write]
            csv_writers[idx%number_of_files].writerow(row_val)

            #for idy in range(len(subrows['Nradar'])):
                #row_dict['Idx'] = idy
                #for label in labels_to_write:
                    #if label not in ['Id', 'Idx', 'Expected']:
                        #row_dict[label] = subrows[label][idy]
                #row_val = [row_dict[col] for col in labels_to_write]
                #csv_writers[idx%number_of_files].writerow(row_val)

    (x.close() for x in output_files)
    return

if __name__ == '__main__':
    split_csv(number_of_files=1)
    split_csv(True, number_of_files=1)
