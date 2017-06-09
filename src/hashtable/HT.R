# This use case demonstrates that hashtable works correctly for file reads.
x <- c(1,2,3,4,5)
y <- c(2,3,4,5,6)
z <- c(3,4,5,6,7)

xy <- data.frame(x,y)
xyz <- data.frame(x,y,z)
write.csv(x, "x.csv")
write.csv(xy, "xy.csv")
write.csv(xyz, "xyz.csv")