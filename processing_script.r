options("repos"="http://cran.at.r-project.org/")
tryCatch(find.package("rgdal"), error=function(e) install.packages("rgdal", dependencies=TRUE))
tryCatch(find.package("raster"), error=function(e) install.packages("raster", dependencies=TRUE))
library("raster")
library("rgdal")
Layer = readOGR("/tmp/processing/16413f8e2315426f89ee8a448caf6084",layer="OUTPUTALGQGISSUMLINELENGTHS2")
Field="length"
Summary_statistics<-data.frame(rbind(sum(Layer[[Field]]),
length(Layer[[Field]]),
length(unique(Layer[[Field]])),
min(Layer[[Field]]),
max(Layer[[Field]]),
max(Layer[[Field]])-min(Layer[[Field]]),
mean(Layer[[Field]]),
median(Layer[[Field]]),
sd(Layer[[Field]])),row.names=c("Sum:","Count:","Unique values:","Minimum value:","Maximum value:","Range:","Mean value:","Median value:","Standard deviation:"))
colnames(Summary_statistics)<-c(Field)
Summary_statistics
