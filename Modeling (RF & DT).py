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
    temp["post_time"]=source["post time"]
    temp["title"]=source["title"]
    temp["content"]=source["content"]
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

# use Foxconn in the modeling first
raw_foxconn = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/2016-2017foxconn.csv", encoding= 'utf-8')
# raw_TSMC = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/2016-2017TSMC.csv", encoding= 'utf-8')
# raw_uni = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/2016-2017uni.csv", encoding= 'utf-8')
foxconn_dead_term = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/each company rise & down/foxconn_down_keyword.csv", encoding= 'utf-8')
foxconn_rise_term = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/each company rise & down/foxconn_up_keyword.csv", encoding= 'utf-8')


foxconn_table=data_table(raw_foxconn)
# print(len(foxconn_table))
foxconn_table.dropna(axis=0, how='any', inplace=True)
# print(len(foxconn_table))
# uni_table=data_table(raw_uni)
# TSMC_table=data_table(raw_TSMC)

dead_term=list(foxconn_dead_term["term"])
rise_term=list(foxconn_rise_term["term"])
foxconn_news=list(foxconn_table["title"]+foxconn_table["content"])
foxconn_news=clean(foxconn_news)
# print(len(foxconn_news))
term=dead_term+rise_term

#count the number of times term appear in the input data (tf)
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
    

tf=data_tf(foxconn_news, term)

# count the df for each term
def data_df(data, term):
    word2id = {}
    id2word = []
    for i, j in enumerate(term):
        word2id[j] = i
        id2word.append(j)

    df = []
    for i in id2word:
        df.append(0)
    for i in id2word:
        for d in data:
            if i in d:
                df[word2id[i]] += 1
    return df


df=data_df(foxconn_news, term)

# delete the term that does not appear in any of the documents(news)
tmp=[]
for i in range(len(df)):
    if df[i] ==0:
        tmp.append(i)
for i in sorted(tmp, reverse=True):
    del term[i]
df=data_df(foxconn_news, term)

def idf(n, df):
    return math.log(n/df)
    
word2id = {}
id2word = []
for i, j in enumerate(term):
    word2id[j] = i
    id2word.append(j)
    

data_dvec=[]
for t in tf:
    tmp=[]
    for i in range(len(term)):
        tmp.append(t[i]*idf(len(foxconn_news), df[i]))
    data_dvec.append(tmp)
#data_dvec=list(map(list, zip(*data_dvec)))

#date is a list of date data, and the output would be a specific date succeeded by an index of the news. We select news two days before
def find_date_index(date, source):
    idx={}
    for j in date:
        temp=[]
        for i in range(len(source)):
            try:  
                if source["post_time"][i]<j+timedelta(days=1) and source["post_time"][i]>=j-timedelta(days=2):
                    temp.append(i)
            except KeyError:
                print(1)
        idx[j]=temp
    return idx

cross_date={"foxconn":["2016/4/11","2016/8/18","2016/11/9","2017/6/14","2017/8/16","2017/11/13","2016/5/27","2016/8/31","2016/12/6","2017/6/19","2017/10/19"],"uni":["2016/4/14","2016/5/13","2016/9/29","2017/1/10","2017/5/11","2017/8/15","2017/10/13","2017/11/14", "2016/3/30","2016/5/6","2016/8/12","2016/11/7","2017/4/12","2017/7/28","2017/9/26","2017/10/24"]}
            #"TSMC":["2016/5/26","2016/12/12","2017/1/6","2017/1/24","2017/3/17","2017/4/27","2017/10/3","2016/4/21","2016/11/4","2016/12/22","2017/1/16","2017/3/7","2017/4/18","2017/9/28","2017/11/28"]}
for i in cross_date:
    for d in range(len(cross_date[i])):
        cross_date[i][d]=datetime.strptime(cross_date[i][d], '%Y/%m/%d')
        

change_vec=[]
s=set()
for i in index:
    s=s|set(index[i])
    for num in index[i]:
        if num<=45769:
            change_vec.append(data_dvec[num])

rest_vec=[]
for k in range(len(data_dvec)):
    if k in list(s):
        pass
    else:
        rest_vec.append(data_dvec[k])
        
dead_x=pd.DataFrame(change_vec)

dead_y=pd.DataFrame(rest_vec)
dead_xy=pd.concat([dead_x, dead_y])
dead_x["results"]=1
# print(len(dead_x))
# print(len(dead_y))
dead_y["results"]=0
final_xy=pd.concat([dead_x, dead_y])


# split the dataset into test and training data
x_train, x_test, y_train, y_test=train_test_split(dead_xy, final_xy[["results"]],test_size=0.2, random_state=0)

forest = ensemble.RandomForestClassifier(n_estimators = 10)

forest_fit = forest.fit(x_train, y_train.values)

clf = tree.DecisionTreeClassifier()
clf.fit(x_train, y_train.values)

# improve until we get higher accuracy
accuracy = metrics.accuracy_score(y_test, clf.predict(x_test))
print(accuracy)


# keywords prediction using 2018 data to check accuracy
foxconn2018 = pd.read_csv("D:/USB/class/fourth/bigdata_analysis/bda2019_dataset/2018_data/2018foxconn.csv", encoding= 'utf-8')
    
foxconn2018=data_table(foxconn2018)
# print(len(foxconn2018))
foxconn2018.dropna(axis=0, how='any', inplace=True)
# print(len(foxconn2018))

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
        if list(predict).count(1)/len(predict)>=0.7:
            final_foxconn[time]="c"
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
