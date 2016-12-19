                                        #
add <- read.csv('../data/addme.csv',header=F)
x <- read.csv('../data/x.csv',header=F)
y <- read.csv('../data/y.csv',header=F)
                                        #
c(apply(add,2,mode),apply(add,2,class))
c(apply(x,2,mode),apply(x,2,class))
c(apply(y,2,mode),apply(y,2,class))

