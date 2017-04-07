### Using RDataTracker to unpack the 
### pitcher-plant food web oxygen model 

### Load RDataTracker and set detail level

library(RDataTracker)
ddg.set.detail(1)

### Run pitcher plant model
ddg.run('./pp_script.R')
ddg.display()
