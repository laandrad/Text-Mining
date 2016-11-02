
setwd("C:/Users/Alejandro/Dropbox/Conference Papers and Projects/Circuit TM/Year 2")

scores1 = read.csv('PIG1quantscores.csv', na.strings = 'X')
colnames(scores1)[1] = 'student'
scores2 = read.csv('PIG2quantscores.csv', na.strings = 'X')
colnames(scores2)[1] = 'student'
PIG1 = read.csv('cosinePIG1.csv')
PIG2 = read.csv('cosinePIG2.csv')

merge(scores1[,1:2], PIG1[,1:2], by = )
