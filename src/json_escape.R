### Test script for issues with JSON parsing
### MKLau

x <- c("Quere\001taro", "Unknown" , " Me\001xico ")
y <- gsub(pattern = "\\\001",replacement = "",x = x)
