source('../src/helpers.R')
library(magrittr)
library(xtable)
refresh <- FALSE

if (refresh){
    ena <- (ls(pos='package:enaR',all.names=TRUE) %>% 
        data.frame %>% 
        write.csv(file = '../../docs/ena_funcs.csv',row.names = FALSE))
    bip <- (ls(pos='package:bipartite',all.names=TRUE) %>% 
        data.frame %>% 
        write.csv(file = '../../docs/bip_funcs.csv',row.names = FALSE))
}


metrics <- (list(nmr = read.csv('../data/ena_funcs.csv'),
                bip = read.csv('../data/bip_funcs.csv')) %>% 
                lapply(function(x) x[x[,2] == 1,]) %>% 
                    do.call(what = rbind))
metrics <- apply(metrics,2,as.character)


met.desc <- list()
for (i in 1:nrow(metrics)){
    if ((paste0(metrics[i,1],'.Rd') %in% 
        dir(paste0('../data/',metrics[i,3],'/man')))){
        met.desc[[i]] <- c(
            metrics[i,3],
            metrics[i,1],
            get.desc(metrics[i,1],paste0('../data/',metrics[i,3],'/man'))[1]
            )
    }else{
        met.desc[[i]] <- c(metrics[i,3],metrics[i,1],'')
    }
}
met.desc <- data.frame(do.call(rbind,met.desc))
colnames(met.desc) <- c('Package','Metric','Desciption')
met.desc[,3] <- sapply(met.desc[,3],function(x) paste(unlist(strsplit(as.character(x)," "))[1:5],collapse=" "))
met.desc <- met.desc[!(grepl('NA',met.desc[,3])),]
met.desc <- met.desc[sapply(met.desc[,3],nchar) < 55,]
print(xtable(met.desc),file = '../results/metric_table.txt',include.rownames = FALSE)


