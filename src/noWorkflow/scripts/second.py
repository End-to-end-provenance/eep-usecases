import csv, pandas

input_file = "r_to_py.csv"
output_file = "../results/py_out.csv"

with open(input_file) as f:
      data = pandas.read_csv(input_file)
      data['Temperature']+=5
      data.to_csv(output_file)
