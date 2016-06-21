#!/usr/bin/env python
import argparse
import os
from parsers import wahoo
from reports import generator


def process_data_file(filename):
    print("Processing " + filename)
    f = open(filename)
    return wahoo.parse(f)


def process_data_dir(data_dir):
    datasets = []
    for (root, dirs, files) in os.walk(data_dir):
        for f in files:
            datasets.append(process_data_file(os.path.join(root, f)))
    return datasets


def main():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)

    parser = argparse.ArgumentParser(description='Process some data.')
    parser.add_argument('data_dir', help='The data directory to process')
    args = parser.parse_args()
    if os.path.isdir(args.data_dir):
        datasets = process_data_dir(args.data_dir)
        # generator.generate_report(data, output_dir)

    else:
        print("The specified directory is not valid: " + args.data_dir)

if __name__ == "__main__":
    main()
