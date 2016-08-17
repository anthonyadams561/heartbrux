#!/usr/bin/env python
import argparse
import os
import numpy as np

from heartbrux import reports
from heartbrux.parsers import wahoo


def process_data_file(filename):
    print("Processing {}".format(filename))
    f = open(filename)
    data = wahoo.parse(f)
    time_delta = data.index[data.size - 1] - data.index[0]
    hours = time_delta / np.timedelta64(1, 'h')
    print("{0} data points extracted over {1:.1f} hours".format(data.size, hours))
    return wahoo.parse(f)


def process_data_dir(data_dir):
    datasets = []
    for (root, dirs, files) in os.walk(data_dir):
        for f in files:
            datasets.append(process_data_file(os.path.join(root, f)))
    return datasets


def main():
    parser = argparse.ArgumentParser(description='Process some data.')
    parser.add_argument('data_dir', help='The directory that contains the input data files')
    parser.add_argument('report_dir', help='The directory to write reports to')
    args = parser.parse_args()
    if os.path.isdir(args.data_dir):
        datasets = process_data_dir(args.data_dir)
        for dataset in datasets:
            reports.generate_report(dataset, args.report_dir)

    else:
        print("The specified directory is not valid: " + args.data_dir)

if __name__ == "__main__":
    main()
