# GGmap routing script by Martin Jung
# Homepage: https://conservationecology.wordpress.com/
##Vector processing=group
##x = string Copenhagen, Denmark
##y = string Berlin, Germany
##type= string driving
##output = output vector
if (!require(ggmap)){print("ggmap not installed. Will install it now");install.packages(ggmap, dependencies = TRUE)}
library(rgdal)
 
r <- route(from=x,to=y,mode=type,structure="route",output="simple",alternatives=F,messaging=F) # get the route
cs <- CRS("+proj=longlat +datum=WGS84 +no_defs") # WGS84 projection
 
l <- Lines(list(Line(r[c("lon","lat")])),ID=paste0(type,"_track"))
sl <- SpatialLines(list(l),cs)
 
data <- data.frame(from=x,to=y,type=type,length_km=sum(r$km,na.rm=T),duration_h=sum(r$hours,na.rm=T))
output <- SpatialLinesDataFrame(sl,data=data,match.ID=F)
