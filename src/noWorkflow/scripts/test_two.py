#!/usr/bin/env python

import csv, pandas

def parse_and_pivot(input_file):
    with open(input_file) as f:
        data = pandas.read_csv(f, header = None)
        pivot = data.transpose()
        return pivot

def get_diff(added, mult, output_file):
    compare = added - mult
    compare.to_csv(output_file)

def main():
    input_file = "../data/first.csv"
    input_value = 2
    output_file = "../results/diff.csv"

    second = parse_and_pivot(input_file)
    added = second.add(input_value)
    mult = second*2
    get_diff(added, mult, output_file)

if __name__ == "__main__":
    main()
