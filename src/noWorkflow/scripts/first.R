library(readr)
data<-read.csv("r_in.csv")

data$Temperature <- data$Temperature + 5

write.csv(data, "r_to_py.csv")