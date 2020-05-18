import numpy as np
import math 
import pandas as pd
from sklearn.svm import SVC
from sklearn import datasets, ensemble, metrics, tree
from operator import itemgetter
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split

foxconn2018 = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/2018_data/2018foxconn.csv", encoding= 'utf-8')
#dead_term = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/each company rise & down/foxconn_down_keyword.csv", encoding= 'utf-8')
#rise_term = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/each company rise & down/foxconn_up_keyword.csv", encoding= 'utf-8')
#dead_term=list(dead_term["term"])
#rise_term=list(rise_term["term"])
#term=dead_term+rise_term

def data_table(source):
    temp={}
    temp["post_time"]=source["time"]
    temp["title"]=source["title"]
    temp["content"]=source["context"]
    columns = sorted(temp.keys())
    temp_table=pd.DataFrame(data=temp, columns=columns)
    temp_table["post_time"]=pd.to_datetime(temp_table['post_time'])
    return temp_table
    
foxconn2018=data_table(foxconn2018)
print(len(foxconn2018))
foxconn2018.dropna(axis=0, how='any', inplace=True)
print(len(foxconn2018))

index=find_date_index(cross_date["foxconn"], foxconn_table)

foxconn2018_date=foxconn2018.set_index("post_time")
dates=sorted(list(set(foxconn2018_date.index)))

foxconn_df=data_df(list(foxconn2018["title"]+foxconn2018["content"]), term)

tmp=[]
for i in range(len(foxconn_df)):
    if foxconn_df[i] ==0:
        tmp.append(i)

for i in sorted(tmp, reverse=True):
    del term[i]
foxconn_df=data_df(list(foxconn2018["title"]+foxconn2018["content"]), term)

word2id = {}
id2word = []
for i, j in enumerate(term):
    word2id[j] = i
    id2word.append(j)
foxconn_tf=data_tf(list(foxconn2018["title"]+foxconn2018["content"]), term)

data_vec=[]
for t in foxconn_tf:
    tmp=[]
    for i in range(len(id2word)):
        tmp.append(t[i]*idf(len(foxconn2018), foxconn_df[i]))
    data_vec.append(tmp)
    

news_bydate={}
for time in dates:
    tmp=[]
    for i in range(len(foxconn2018)):
        if i==5162:
            print(2)
        elif time==foxconn2018["post_time"][i]:
            tmp.append(i)
    news_bydate[time]=tmp


def get_vec(total_vec, index):
    tmp=[]
    for i in index:
        tmp.append(data_vec[i])
    return tmp
    
#random forest的prediction
final_foxconn={}
for time in news_bydate:
    if time!= datetime(2018,1,1) and time!=datetime(2018,1,2):
        news=[]
        try:    
            news=get_vec(data_vec, news_bydate[time-timedelta(days=2)])
        except:
            print(1)
        try:
            news=news+get_vec(data_vec, news_bydate[time-timedelta(days=1)])
        except KeyError:
            print(2)
        try:
            news=news+get_vec(data_vec, news_bydate[time])
        except Keyerror:
            print(3)
        test=pd.DataFrame(news)
        predict=forest.predict(test)
        if list(predict).count(1)/len(predict)>=0.7:
            final_foxconn[time]="c"
        else:
            final_foxconn[time]="n"
            

#decisoin tree的prediction
final_foxconn={}
for time in news_bydate:    
    try:    
        news=get_vec(data_vec, news_bydate[time-timedelta(days=2)])
    except:
        print(1)
    try:
        news=news+get_vec(data_vec, news_bydate[time-timedelta(days=1)])
    except KeyError:
        print(2)
    try:
        news=news+get_vec(data_vec, news_bydate[time])
    except Keyerror:
        print(3)
    test=pd.DataFrame(news)
    predict=clf.predict(test)

    if list(predict).count(1)/len(predict)>=0.7:
        final_foxconn[time]="c"
    else:
        final_foxconn[time]="n"
        

date=[]
results=[]
for i in final_foxconn:
    date.append(i)
    results.append(final_foxconn[i])


t=pd.DataFrame({'post_time':date, 'predict_results':results})
t.to_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/2018_data/request2/TSMC_decision-tree_predict_result.csv")
