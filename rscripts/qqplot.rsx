##Plots=group
##showplots
##Layer=vector
##X=Field Layer
#qqnorm(Layer[[X]])
#qqline(Layer[[X]])
library("ggplot2")

ggplot() + geom_point(aes(Layer[[X]]))