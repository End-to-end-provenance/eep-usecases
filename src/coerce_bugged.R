for (i in 1:2){
    assign(paste0('x',i),
           matrix(sample(1:100,100,replace=TRUE),nrow=10))
}
y <- x1
