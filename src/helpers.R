
get.desc <- function(x = 'function name',man.loc = 'manual location'){
    man <- readLines(paste0(man.loc,'/',x,'.Rd'))
    man[grep('description',man,T) + 1]
}

