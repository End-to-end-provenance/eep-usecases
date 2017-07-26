import pandas, csv

with open('x_pandas.csv') as csvfile:
    data = pandas.read_csv(csvfile)

with open('xy_pandas.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    # https://stackoverflow.com/questions/26464567/csv-read-specific-row
    rows = [r for r in csvreader]

x = rows[0]
y = rows[1]
