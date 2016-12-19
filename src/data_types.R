### "add": has header, all values quoted
### has the letter "l" in line 9
add <- read.csv('../data/addme.csv',header=T)
c(apply(add,2,mode),apply(add,2,class))
### "x": no header, no values quoted
### has the letter "l" in line 9
x <- read.csv('../data/x.csv',header=F)
c(apply(x,2,mode),apply(x,2,class))
### "y": no header, no values quoted
### only numbers
y <- read.csv('../data/y.csv',header=F)
c(apply(y,2,mode),apply(y,2,class))
