# This use case demonstrates that hashtable works correctly for a series of 
# file reads and writes.
x <- read.csv("x.csv")
xy <- read.csv("xy.csv")
write.csv(x,"x2.csv")
xyz <- read.csv("xyz.csv")
write.csv(xy,"xy2.csv")
write.csv(xyz,"xyz2.csv")