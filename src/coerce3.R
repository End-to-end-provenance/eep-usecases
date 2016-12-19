### In this case, a user would expect the data
### to be numeric; however, someone has inserted
### a typo in line 9 and changed what should be
### the number one (i.e. "1") to the letter "l". 
### NOTE: these data are identical to those in
### data/y.csv with exception of the "l" that is
### on line 9.
                                        #
x <- read.csv('../data/x.csv',header=F)
sum(x)
