##[Sehra]=group
##showplots
##Layer=vector
##Field=Field Layer
# hist(Layer[[Field]],main=paste("Histogram of",Field),xlab=paste(Field))


plot(Layer[["Direct Cos"]])
lines(Layer[["Aggregated"]], type = "o", col = "blue")

