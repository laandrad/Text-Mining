library(dplyr)
library(RColorBrewer)

file = "C:/Users/Alejandro/Desktop/output/Koalas_cosine.csv"

dat = file %>% read.csv
t = dat$time %>% as.POSIXlt(., format = '%H:%M:%S')
n = dat$subject %>% unique %>% length

dat$X2_expert1 %>% tapply(., dat$subject, mean)

mypalette = brewer.pal(n, 'Set2')

## Similarity with Expert ####
plot(t, dat$X2_expert1, type = 'n', xlab = 'Time', ylab = 'Similarity', 
     main = 'Group Koalas -- Similarity with Expert')

for (i in 1:n) {
  d = subset(dat, dat$subject == i)
  td = as.POSIXlt(d$time, format = '%H:%M:%S')
  
  lines(td, d$X2_expert1, col = mypalette[i], lty = i + 3, lwd = 2)
}
xl = t %>% max
yl = dat$X2_expert1 %>% max
legend(xl - 240, yl, paste('Student', 1:n), col = mypalette[1:(n + 1)], cex = .75, lwd = 2, lty = 1:n + 3, bty = 'n')


## Similarity with Students ####
plot(t, dat$s.s16post, type = 'n', xlab = 'Time', ylab = 'Similarity', 
     main = 'Group Koalas -- Similarity with Student 1')

for (i in 1:n) {
  d = subset(dat, dat$subject == i)
  td = as.POSIXlt(d$time, format = '%H:%M:%S')
  
  lines(td, d$s.s16post, col = mypalette[i], lty = i + 3, lwd = 2)
}

yl = dat$s.s16post %>% max
legend(xl - 240, yl, paste('Student', 1:n), col = mypalette[1:(n + 1)], cex = .75, lwd = 2, lty = 1:n + 3, bty = 'n')
