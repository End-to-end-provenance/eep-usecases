import csv, os, pandas

input_file = "output.csv"
output_file = "../results/results.csv"

with open(input_file) as f:
      data = pandas.read_csv(input_file)
      data['Temperature']+=10
      data.to_csv(output_file)
