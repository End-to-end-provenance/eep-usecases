### This script conducts a null model based
### analysis of the an ecosystem network model.

library(enaR)
library(bipartite)

## set the seed value for future replication
set.seed(12345)

## load the model 
data(enaModels)
data(enaModelInfo)
model <- as.matrix(enaModels[[9]])

## calculate observed nestedness
model.nest <- nested(model)

## simulate from null model
null.models <- shuffle.web(model,3) 
null.nest <- unlist(lapply(null.models,FUN=nested))

## calculate null model statistics
stats <- c(ses = (model.nest - mean(null.nest)) / sd(null.nest),
           pval = length(null.nest[null.nest <= model.nest]) / length(null.nest))

## print stats
print(stats)

## record the seed
.Random.seed
