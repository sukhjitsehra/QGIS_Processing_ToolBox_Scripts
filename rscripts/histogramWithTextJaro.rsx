##my_group=group
##showplots
##Layer=vector
##a=Field Layer
library("ggplot2")
#more = a>0.3
dat <- data.frame(a>0.3 )

ggplot() + geom_bar(aes(Layer[[a]],fill=a > 0.300))+geom_text(size = 3)+xlab(a)+ylab("count")+theme_bw()+ggtitle("Distribution of Jaro-Winkler Distance")



