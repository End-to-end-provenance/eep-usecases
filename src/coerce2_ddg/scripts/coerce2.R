### Here a user imports and checks the data.
### She then combines these data with a matrix
### that she creates in R. The script fails at 
### the point of trying to do a summation.
                                        # data import
y <- read.csv('../data/y.csv',header=F)
                                        # data check
c(apply(y,2,mode),apply(y,2,class))
                                        # data creation
new.y <- matrix(c(1,2,3,4,5,'l',2,3,4,5),nrow=5)
                                        # data binding
y <- rbind(y,new.y)
                                        # apply to summarize data
sum(y)
