
# install.packages('LearnBayes')
library(LearnBayes)

# proportion p vector:
p = seq(0.05, 0.95, by = 0.1); p


# corresponding weights
prior = c(1, 5.2, 8, 7.2, 4.6, 2.1, 0.7, 0.1, 0, 0); prior

# prior probabilities of each p proportion
prior = prior/sum(prior); prior

plot(p, prior, type = "h", ylab="Prior Probability")

data = c(11, 16); data

# posterior densities
post = pdisc(p, prior, data)
post



