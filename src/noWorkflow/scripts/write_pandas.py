import csv, pandas

x = [i for i in range(0,6)]
y = [i for i in range(1,7)]
z = [i for i in range(2,8)]

df = pandas.DataFrame(x)
df.to_csv('x_pandas.csv', index=False, header=False)

data = []
data.append(x)
data.append(y)

df = pandas.DataFrame(data)

df.to_csv('xy_pandas.csv', index=False, header=False)
