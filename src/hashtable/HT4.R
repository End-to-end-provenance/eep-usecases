# This use case demonstrates that hashtable works correctly for file reads.
q <- c(1,2,3,4,5)
r <- c(2,3,4,5,6)
s <- c(3,4,5,6,7)

qr <- data.frame(q,r)
qrs <- data.frame(q,r,s)
write.csv(q, "q.csv")
write.csv(qr, "qr.csv")
write.csv(qrs, "qrs.csv")