#!/usr/bin/python

import os
import gzip
import csv

import numpy as np

nan_vals = [-99900, -99901, -99903, 999]

def count_decreasing(x):
    temp = np.fromstring(x, sep=' ')
    numb = 1
    arr = [0]
    prev = temp[0]
    for idx in range(1,len(temp)):
        if temp[idx] > prev:
            numb += 1
        prev = temp[idx]
        arr.append(numb)
    return np.array(arr)

def count_distances(x):
    temp = np.fromstring(x, sep=' ')
    numb = 1
    arr = [0]
    prev = temp[0]
    for idx in range(1,len(temp)):
        if temp[idx] != prev:
            numb += 1
        prev = temp[idx]
        arr.append(numb)
    return np.array(arr)

def per_radar_average(arr, ridx):
    numb = ridx[-1]+1
    ravg = numb*[0]
    navg = numb*[0]
    for a, r in zip(arr,ridx):
        if np.isnan(a) or any(int(a) == int(n) for n in nan_vals):
            continue
        ravg[r] += a
        navg[r] += 1
    favg = []
    for r, n in zip(ravg,navg):
        if n > 0 :
            favg.append(r/n)
    sumfavg = sum(favg)
    if len(favg) > 0 and not np.isnan(sumfavg):
        return sum(favg)/len(favg)
    else:
        return np.nan

def split_csv(is_test=False, number_of_files=1):
    orig_csv_file = 'train_2013.csv.gz'
    output_prefix = 'train_2013_avg'
    if is_test:
        orig_csv_file = 'test_2014.csv.gz'
        output_prefix = 'test_2014_avg'

    if number_of_files == 1:
        output_files = [gzip.open('%s.csv.gz' % output_prefix, 'w')]
    else:
        output_files = [gzip.open('%s_%d.csv.gz' % (output_prefix, n), 'w') for n in range(10)]
    csv_writers = [csv.writer(f) for f in output_files]

    labels_to_write = ['Id', 'RadarId', 'Composite', 'HybridScan', 'HydrometeorType', 'Kdp', 'RR1', 'RR2', 'RR3', 'RadarQualityIndex', 'Reflectivity', 'ReflectivityQC', 'RhoHV', 'Velocity', 'Zdr', 'LogWaterVolume', 'MassWeightedMean', 'MassWeightedSD']
    if not is_test:
        labels_to_write.append('Expected')

    labels_to_avg = ['Composite', 'HybridScan', 'HydrometeorType', 'Kdp', 'RR1', 'RR2', 'RR3', 'RadarQualityIndex', 'Reflectivity', 'ReflectivityQC', 'RhoHV', 'Velocity', 'Zdr', 'LogWaterVolume', 'MassWeightedMean', 'MassWeightedSD']

    with gzip.open(orig_csv_file, 'r') as infile:
        csv_reader = csv.reader(infile)
        labels = next(csv_reader)
        for c in csv_writers:
            c.writerow(labels_to_write)
        for idx, row in enumerate(csv_reader):
            if idx == 100:
                break
            row_dict = dict(zip(labels, row))
            
            time_idx = count_decreasing(row_dict['TimeToEnd'])
            dist_idx = count_distances(row_dict['DistanceToRadar'])
            
            max_idx = np.max([time_idx, dist_idx], axis=0)
            row_dict['RadarId'] = max_idx[-1]+1
            
            for col in labels_to_avg:
                arr = np.fromstring(row_dict[col], sep=' ')
                row_dict[col] = per_radar_average(arr, max_idx)
                
            row_val = [row_dict[col] for col in labels_to_write]
            
            csv_writers[idx%number_of_files].writerow(row_val)
            
    (x.close() for x in output_files)
    return

if __name__ == '__main__':
    split_csv(number_of_files=1)
    split_csv(True, number_of_files=1)
