### Script for using the codecleanR function
### to clean some messy code.

### Generate the provenance for your code
library(RDataTracker)
ddg.set.detail(0)
ddg.run('messycode.R')

### Get info about codecleanR
system('codecleanR -h')

### Get a plot of your code's prov-graph
system('codecleanR --svg messycode_ddg/ddg.json')
system('open graph.svg')

### Get info about items in your graph
system('codecleanR --info messycode_ddg/ddg.json')

### Get cleaned code for specific output
system('codecleanR --code messycode_ddg/ddg.json d20 > messycode_cleaned.R')
