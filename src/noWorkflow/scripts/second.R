data<-read.csv("output.csv")

data$Temperature <- data$Temperature + 5

write.csv(data, "r_out.csv")