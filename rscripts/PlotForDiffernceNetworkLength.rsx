##Vector processing=group
##showplots
##Layer=vector
##a=Field Layer
##b=Field Layer
library("ggplot2")

ggplot() + 
geom_point(aes(Layer[[ID]], Layer[[Difference]]))