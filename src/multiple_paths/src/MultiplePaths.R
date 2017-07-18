data <- read.csv("Data.csv")
numAnimals <- nrow(data)
totalLegs <- sum(data$Legs)
summary <- data.frame(numAnimals, totalLegs)
write.csv(summary, "summary.csv")

