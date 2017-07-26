import csv, pandas

input_file = "../data/test_one_data.csv"
output_file = "../results/test_one_results.csv"

data = pandas.read_csv(input_file)

data['carb']/=0.1
data['optden']/=0.086

for i in range (0, len(data.columns)):
    data['carb'] = round(data['carb'], 0)

for i in range (0, len(data.columns)):
    data['optden'] = round(data['optden'], 2)

data.to_csv(output_file)
