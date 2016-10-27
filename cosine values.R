library(lsa)
library(dplyr)

student.list = function(path){
  stList = list.files(path = , path, pattern = '*.txt')
  st = NULL
  for(i in 5:length(stList)) st[i] = gsub('pre.txt', '', stList[i])
  for(i in 1:length(st)) st[i] = gsub('group.txt', '', st[i])
  for(i in 1:length(st)) st[i] = gsub('post.txt', '', st[i])
  
  st = st[!is.na(st)]
  for(i in 1:length(st)) st[i] = gsub('s', '', st[i])
  st = as.numeric(st)
  st = st[order(st)]
  return(st)
}

pre.post.cosine = function(x){
  path = paste0(wd, paste0('/', c('pre', 'during', 'post')))
  sl.pre = student.list(path[1])
  sl.dur = student.list(path[2])
  sl.post = student.list(path[3])
  
  setwd(wd)
  temp = list.files(pattern="*.csv") # read files in folder
  
  pre = read.csv(temp[3])
  pre[13,]
  d = cosine(t(pre))
  st.cos.pre = d[5:nrow(d),1:4]
  st.cos.pre = as.data.frame(st.cos.pre)
  colnames(st.cos.pre) = paste0('pre.exp', 1:4)
  st.cos.pre$student = sl.pre

  during = read.csv(temp[1])
  d = cosine(t(during))
  st.cos.during = d[5:nrow(d),1:4]
  st.cos.during = as.data.frame(st.cos.during)
  colnames(st.cos.during) = paste0('dur.exp', 1:4)
  st.cos.during$student = sl.dur
 
  post = read.csv(temp[2])
  d = cosine(t(post))
  st.cos.post = d[5:nrow(d),1:4]
  st.cos.post = as.data.frame(st.cos.post)
  colnames(st.cos.post) = paste0('post.exp', 1:4)
  st.cos.post$student = sl.post
  
  dat = merge(st.cos.pre, st.cos.during, by = 'student')
  dat = merge(dat, st.cos.post, by = 'student')
  dat[is.na(dat)] = 0
  
  return(dat)
}

wd = "C:/Users/Alejandro/Dropbox/Conference Papers and Projects/Circuit TM/Year 2/PIG1"
PIG1 = pre.post.cosine(wd)

wd = "C:/Users/Alejandro/Dropbox/Conference Papers and Projects/Circuit TM/Year 2/PIG2"
PIG2 = pre.post.cosine(wd)
