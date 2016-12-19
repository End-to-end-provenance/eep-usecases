### Here, the user is working on combining two
### input data frames but isn't checking the
### data when it is imported. The error results
### after the two dataq sets are combined.
                                        # import the data
y <- read.csv('../data/y.csv',header=F)
x <- read.csv('../data/x.csv',header=F)
                                        # sum of y
sum(y)
                                        # binding data
z <- cbind(y,x)
                                        # sum of y combined with x
apply(x,2,sum)
