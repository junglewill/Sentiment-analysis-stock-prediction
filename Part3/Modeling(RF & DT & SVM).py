import numpy as np
import math 
import pandas as pd
from sklearn.svm import SVC
from sklearn import datasets, ensemble, metrics, tree
from operator import itemgetter
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split

def data_table(source):
    temp={}
    temp["post_time"]=source["time"]
    temp["title"]=source["title"]
    temp["content"]=source["context"]
    columns = sorted(temp.keys())
    temp_table=pd.DataFrame(data=temp, columns=columns)
    temp_table["post_time"]=pd.to_datetime(temp_table['post_time'])
    return temp_table
    
def clean(source):
    temp=[]
    for i in source:
        if str(i)!="nan":
            temp.append(i)
    return temp

# we chose the rise and decline terms used in part1
dead_term = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/dead_keyword.csv", encoding= 'utf-8')
rise_term = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/rise_keyword.csv", encoding= 'utf-8')
dead_news = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/total_company_up & down/bda2019_mid_project_down.csv", encoding= 'utf-8')
rise_news = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/total_company_up & down/bda2019_mid_project_up.csv", encoding= 'utf-8')

dead_term=list(dead_term["term"])
rise_term=list(rise_term["term"])
dead_news=list(dead_news["title"]+dead_news["content"])
rise_news=list(rise_news["title"]+rise_news["content"])
dead_news=clean(dead_news)
rise_news=clean(rise_news)

#term=dead_term+rise_term

word2id = {}
id2word = []
for i, j in enumerate(term):
    word2id[j] = i
    id2word.append(j)
    
#count the number of times term appear in each data sources (tf) 
def data_tf(data, term):
    word2id = {}
    id2word = []
    for i, j in enumerate(term):
        word2id[j] = i
        id2word.append(j)

    tf = []
    for d in data:
        tmp = []
        for i in id2word:
            tmp.append(d.count(i))
        tf.append(tmp)
    return tf
    
    
dtf=data_tf(dead_news, term)

rtf=data_tf(rise_news, term)

# count the df value for each term
def data_df(data, term):
    word2id = {}
    id2word = []
    for i, j in enumerate(term):
        word2id[j] = i
        id2word.append(j)

    df = []
    for i in id2word:
        df.append(0)
        for d in data:
            if i in d:
                df[word2id[i]] += 1
    return df
    
ddf=data_df(dead_news, term)
rdf=data_df(rise_news,term)

def idf(n, df):
    return math.log(n/df)

data_dvec=[]
for tf in dtf:
    tmp=[]
    for i in range(len(id2word)):
        tmp.append(tf[i]*idf(len(dead_news), ddf[i]))
    data_dvec.append(tmp)
#data_dvec=list(map(list, zip(*data_dvec)))

data_rvec=[]
for tf in rtf:
    tmp=[]
    for i in range(len(id2word)):
        tmp.append(tf[i]*idf(len(rise_news), rdf[i]))
    data_rvec.append(tmp)
#data_rvec=list(map(list, zip(*data_rvec)))

dead_x=pd.DataFrame(data_dvec)
dead_y=pd.DataFrame(data_dvec)
dead_y["results"]=0
rise_x=pd.DataFrame(data_rvec)
rise_y=pd.DataFrame(data_rvec)
rise_y["results"]=1

x_train, x_test, y_train, y_test=train_test_split(pd.concat([dead_x, rise_x]), pd.concat([dead_y, rise_y])[["results"]],test_size=0.2, random_state=0)

# Random forest modeling
forest = ensemble.RandomForestClassifier(n_estimators = 10)

forest_fit = forest.fit(x_train, y_train.values)

svm=SVC(kernel="linear", probability=True)
svm.fit(x_train, y_train.values)

clf = tree.DecisionTreeClassifier()
clf.fit(x_train, y_train.values)

error=0
for i, v in enumerate(clf.predict(x_test)):
    if v!= y_test.values[i]:
        error=error+1
# print(error)
# print(len(clf.predict(x_test)))

accuracy = metrics.accuracy_score(y_test, clf.predict(x_test))
# print(accuracy)

foxconn2018 = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/2018_data/2018uni.csv", encoding= 'utf-8')
dead_term = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/dead_keyword.csv", encoding= 'utf-8')
rise_term = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/rise_keyword.csv", encoding= 'utf-8')
dead_term=list(dead_term["term"])
rise_term=list(rise_term["term"])
term=dead_term+rise_term

foxconn2018=data_table(foxconn2018)
print(len(foxconn2018))
foxconn2018.dropna(axis=0, how='any', inplace=True)
print(len(foxconn2018))

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

news_bydate={}
for time in dates:
    tmp=[]
    for i in range(len(foxconn2018)):
        if i==5162:
            print(2)
        elif time==foxconn2018["post_time"][i]:
            tmp.append(i)
    news_bydate[time]=tmp
    
data_vec=[]
for t in foxconn_tf:
    tmp=[]
    for i in range(len(id2word)):
        tmp.append(t[i]*idf(len(foxconn2018), foxconn_df[i]))
    data_vec.append(tmp)
    
def get_vec(total_vec, index):
    tmp=[]
    for i in index:
        tmp.append(data_vec[i])
    return tmp
    
#random forest prediction
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
        if list(predict).count(0)/len(predict)>=0.7:
            final_foxconn[time]="f"
        elif list(predict).count(1)/len(predict)>=0.7:
            final_foxconn[time]="u"
        else:
            final_foxconn[time]="n"

#decisoin tree prediction
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
    if list(predict).count(0)/len(predict)>=0.7:
        final_foxconn[time]="f"
    elif list(predict).count(1)/len(predict)>=0.7:
        final_foxconn[time]="u"
    else:
        final_foxconn[time]="n"
        
#SVM prediction
final_foxconn={}
for time in news_bydate:
    if time!= datetime(2018,1,1) and time!=datetime(2018,1,2):
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
        predict=svm.predict(test)
        if list(predict).count(0)/len(predict)>=0.7:
            final_foxconn[time]="f"
        elif list(predict).count(1)/len(predict)>=0.7:
            final_foxconn[time]="u"
        else:
            final_foxconn[time]="n"


date=[]
results=[]
for i in final_foxconn:
    date.append(i)
    results.append(final_foxconn[i])



t=pd.DataFrame({'post_time':date, 'predict_results':results})
t.to_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/2018_data/uni_forest_predict_result.csv")

t=pd.DataFrame({'post_time':date, 'predict_results':results})
t.to_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/2018_data/uni_decision-tree_predict_result.csv")
