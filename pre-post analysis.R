setwd("C:/Users/Alejandro/Dropbox/Conference Papers and Projects/Circuit TM/Year 2")

library(coin)

scores1 = read.csv('PIG1quantscores.csv', na.strings = 'X')
colnames(scores1)[1] = 'student'
scores2 = read.csv('PIG2quantscores.csv', na.strings = 'X')
colnames(scores2)[1] = 'student'
PIG1 = read.csv('cosinePIG1.csv')
PIG2 = read.csv('cosinePIG2.csv')

pre_post = function(dat){
  dat = dat[complete.cases(dat),]

  stats = round(apply(dat, 2, median),3)
  print('Summary Statistics: Medians')
  print(stats)

  phase = rep(c('pre','post'), each = nrow(dat))
  level = as.numeric(unlist(list(dat[,1], dat[,2])))
  wt = wilcoxsign_test(dat[,1]~ dat[,2], distribution='exact', conf.int=T)
  print(wt)

  correl = cor(scores1$Individual, scores1$Final.Group, use = 'complete.obs', method = "spearman")
  print(paste('correlation:', round(correl,3)))
}

pre_post(scores1[,c(2,4)])
pre_post(scores2[,c(2,4)])
pre_post(PIG1[,c(2,10)])
pre_post(PIG2[,c(2,10)])

