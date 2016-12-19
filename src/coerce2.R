y <- read.csv('../data/x.csv',header=F)

### Create matrices
x1 <- matrix(sample(1:100,100,replace=TRUE),nrow=10)
x2 <- matrix(sample(1:100,100,replace=TRUE),nrow=10)
x3 <- matrix(sample(1:100,100,replace=TRUE),nrow=10)
y <- read.csv('../data/addme.csv',header=F)

### Bind them together
x1x3 <- cbind(x1,x3)
x1x2 <- cbind(x1,x2)
x1y <- cbind(x1,y)

### Get the colum-wise sum
apply(x1x3,2,sum)
apply(x1x2,2,sum)
apply(x1y,2,sum)
