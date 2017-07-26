from urllib.request import urlopen

#------------------ SPLIT LOGGER FILE ---------------------#

metsta_url = "http://harvardforest.fas.harvard.edu/sites/harvardforest.fas.harvard.edu/files/weather/metsta.dat"

m101 = open("m101.csv", "w")
m102 = open("m102.csv", "w")

with urlopen(metsta_url) as response:
    for line in response:
        line = line.decode("utf-8")
        if line[0:3] == "101":
            m101.write(line)
        else:
            m102.write(line)

m101.close()
m102.close()
