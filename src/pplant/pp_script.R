### Simulation using the pitcher plant model
if (!'sarModel' %in% installed.packages()[,1]){
    if (!'devtools' %in% installed.packages()[,1]){install.packages('devtools')}
    library(devtools)
    install_github('HFpostdoc/sarModel','develop')
}
library('sarModel')

### this is the normal run of the model
sim <- ppSim(3)

### this is the unpacked version

days <- 3
foodWeight <- 1
beta <- 4.5e-06
d <- 5
k <- 2
Amax <- 20
Amin <- Amax/1.5
m <- 0
aMax <- 2 
aMin <- 1
s <- 1
feedingTime <- 720
c <- 1
x0 <- 0
w0 <- 0
w.w <- 75
photo.val <- 1
Ascalar <- 0.75
Bscalar <- 1
bound.max <- FALSE
verbose <- FALSE 
decycle <- FALSE 

if (length(foodWeight) < days){ 
    foodWeight <- rep(foodWeight,days)[1:days] 
}
    ## Initialization ##
                                        # time keeper
    minute <- 1
                                        # simulate photosynthesis as fixed values
    P <- photo(days,(Amax/Amax),(Amax/Amin - 1))
    if (decycle){cyc <- P}
                                        # food weight at time 1
    if (feedingTime == 1){
        w <- w0 + foodWeight[1]
    }else{w <- w0}
                                        # initial nutrient value
    n <- mineralization(x0,w[1],c)
                                        # initial augmentation value
    a <- augmentation(n[length(n)],s,d,aMin,aMax)
                                        # initial biological o2 demand
    B <- Amax * ((a * Bscalar) * (w[1]/(k+w[1]))) 
                                        # augmented photosynthesis initialization
    A <- Amax * ((a * Ascalar) * P[1])
                                        # o2 at minute=0, P=0 b/c unable to index at minute=0
    x <- A[length(minute)] - (m + B[length(minute)])
                                        #start day loop
    for (z in 1:days){
                                        #star minute loop
        for (j in 1:1440){
            if (verbose){print(c(z,j,minute[length(minute)]))}
                                        # update #
                                        # time keeper
            minute <- c(minute,minute[length(minute)] + 1)
                                        # food weight at t
            wt <- decomp(w[length(minute) - 1],beta=beta,w.w=w.w)
            if (j == feedingTime){
                w <- c(w,wt + foodWeight[z])
            }else{
                w <- c(w,wt)
            }
                                        # nutrient value
            n <- c(n,mineralization(x[length(minute) - 1],w[length(minute)], c))
                                        # augmentation value
            a <- c(a,augmentation(n[length(n)],s,d,aMin,aMax))
                                        # biological o2 demand
            B <- c(B,
                   (Amax * 
                        ((a[length(minute)] * Bscalar) * 
                             (w[length(minute)] / (k + w[length(minute)])))))
                                        # augmented photosynthesis initialization
            A <- c(A,(Amax * (a[length(minute)] * Ascalar) * P[length(minute)]))
                                        # o2 at minute=0, P=0 b/c unable to index at minute=0
            x <- c(x, A[length(minute)] - (m + B[length(minute)]))
            if (is.na(x[length(x)])){x[length(x)] <- 0}
            if (x[length(x)] < 0){x[length(x)] <- 0}
            if (bound.max & x[length(x)] > aMax){x[length(x)] <- aMax}
        } # end minute loop
    } # end day loop
                                        # trim objects to appropriate time
                                        # omitted values aren't relevant
    minute <- minute[1:length(P)]
    Control <- (P * Amax * (augmentation(0,s,d,aMin,aMax) * Ascalar))
    A <- A[1:length(P)]
    B <- B[1:length(P)]
    n <- n[1:length(P)]
    a <- a[1:length(P)]
    if (decycle){x <- x[1:length(P)] - Control}else{x <- x[1:length(P)]}
    w <- w[1:length(P)]
                                        # prep for export
    data <- data.frame(minute, x, Control, A, B, w, n, a)
    colnames(data) <- c("Minute", "Oxygen", "Control","Photosynthesis",
                        "Biological Oxygen Demand", "Food Amount", 
                        "Nutrients","Augmentation Value")

