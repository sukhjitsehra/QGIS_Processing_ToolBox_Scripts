##[Sehra]=group
##showplots
##Layer=vector
##X=Field Layer
library(ggplot2)
#qplot(Layer[[X]])
plot(density(log10(Layer[[X]]). adjust=0.5))

