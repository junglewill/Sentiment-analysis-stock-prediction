# coding: utf-8

# In[1]:


import math
import pandas as pd
import numpy as np
from operator import itemgetter
from datetime import datetime, timedelta
raw_bbs = pd.read_csv("/Users/leepinghsun/Desktop/bda2019_dataset/bbs.csv", encoding= 'utf-8')
raw_forum = pd.read_csv("/Users/leepinghsun/Desktop/bda2019_dataset/forum.csv", encoding= 'utf-8')
raw_news = pd.read_csv("/Users/leepinghsun/Desktop/bda2019_dataset/news.csv", encoding= 'big5')

dead_cross_date={"foxconn":["2018/2/5","2018/3/31","2018/6/19","2018/8/17"],"uni":["2018/2/8","2018/8/8","2018/10/15","2018/11/12","2018/11/26"],"TSMC":["2018/2/9","2018/3/29","2018/6/21","2018/10/5","2018/12/7"]}
for i in dead_cross_date:
    for d in range(len(dead_cross_date[i])):
        dead_cross_date[i][d]=datetime.strptime(dead_cross_date[i][d], '%Y/%m/%d')
golden_cross_date={"foxconn":["2018/1/19","2018/3/13","2018/5/15","2018/7/19"],"uni":["2018/3/2","2018/8/17","2018/11/19"],"TSMC":["2018/1/4","2018/3/12","2018/6/6","2018/7/10","2018/12/3"]}
for i in golden_cross_date:
    for d in range(len(golden_cross_date[i])):
        golden_cross_date[i][d]=datetime.strptime(golden_cross_date[i][d], '%Y/%m/%d')

def clean(source):
    temp=[]
    for i in source:
        if str(i)!="nan":
            temp.append(i)
    return temp

def data_table(source):
    temp={}
    temp["post_time"]=source["post_time"]
    temp["title"]=source["title"]
    temp["content"]=source["content"]
    columns = sorted(temp.keys())
    temp_table=pd.DataFrame(data=temp, columns=columns)
    temp_table["post_time"]=pd.to_datetime(temp_table['post_time'])
    return temp_table

bbs_table=data_table(raw_bbs)
forum_table=data_table(raw_forum)
news_table=data_table(raw_news)

#source放的是上面整理過的table
def maketolist(source):
    temp=list(source["title"]+source["content"])
    return temp

#date為日期的list, 輸出的是某個日期後面接(新聞的index)
def find_date_index(date, source, index):
    idx={}
    for j in date:
        temp=[]
        for i in index:
            if source["post_time"][i]<j+timedelta(days=1) and source["post_time"][i]>=j-timedelta(days=2):
                temp.append(i)
        idx[j]=temp
    return idx

#keywords放上面的list，source放的是maketolist的東西
def find_keyword_index(keyword, keyword_list, source):
    temp=[]
    for i in range(len(source)):
        if type(source[i])!=str:
            source[i]=str(source[i])
        for words in keyword_list:
            if words in source[i]:
                temp.append(i)
                break
    return temp

key_TSMC = ["台積電", "張忠謀", "劉德音", "魏哲家", "晶圓", "代工", "奈米", "製程", "半導體", "晶片", "積體", "電路"]
key_foxconn = ["鴻海", "夏普", "台積電", "指數", "外資", "法人", "供應鏈", "和碩", "友達", "日月光"]
key_uni =["統一", "零售", "物流", "食品", "加工", "棒球", "味全", "超商", "兄弟", "星巴克", "百貨"]


idx={}
idx["bbstable_foxconn"]=find_keyword_index("foxconn", key_foxconn, maketolist(bbs_table))
idx["forumtable_foxconn"]=find_keyword_index("foxconn", key_foxconn, maketolist(forum_table))
idx["newstable_foxconn"]=find_keyword_index("foxconn", key_foxconn, maketolist(news_table))
idx["bbstable_TSMC"]=find_keyword_index("TSMC", key_TSMC, maketolist(bbs_table))
idx["forumtable_TSMC"]=find_keyword_index("TSMC", key_TSMC, maketolist(forum_table))
idx["newstable_TSMC"]=find_keyword_index("TSMC", key_TSMC, maketolist(news_table))
idx["bbstable_uni"]=find_keyword_index("uni", key_uni, maketolist(bbs_table))
idx["forumtable_uni"]=find_keyword_index("uni", key_uni, maketolist(forum_table))
idx["newstable_uni"]=find_keyword_index("uni", key_uni, maketolist(news_table))

#某個日期的前兩天星聞，這邊的index是上面的func輸出後的某個日期的東西
def get_data(source, index):
    result =pd.DataFrame(columns=('post_time','title','content'))
    for i in range(len(index)):
        result.loc[i]=source.loc[index[i]]
    return result

bbstable_dead_foxconn_date=find_date_index(dead_cross_date["foxconn"],bbs_table, idx["bbstable_foxconn"])
bbstable_dead_uni_date=find_date_index(dead_cross_date["uni"],bbs_table, idx["bbstable_uni"])
bbstable_dead_TSMC_date=find_date_index(dead_cross_date["TSMC"],bbs_table, idx["bbstable_TSMC"])

forumtable_dead_foxconn_date=find_date_index(dead_cross_date["foxconn"],forum_table, idx["forumtable_foxconn"])
forumtable_dead_uni_date=find_date_index(dead_cross_date["uni"],forum_table, idx["forumtable_uni"])
forumtable_dead_TSMC_date=find_date_index(dead_cross_date["TSMC"],forum_table, idx["forumtable_TSMC"])

newstable_dead_foxconn_date=find_date_index(dead_cross_date["foxconn"],news_table, idx["forumtable_foxconn"])
newstable_dead_uni_date=find_date_index(dead_cross_date["uni"],news_table, idx["forumtable_uni"])
newstable_dead_TSMC_date=find_date_index(dead_cross_date["TSMC"],news_table, idx["forumtable_TSMC"])

def combine_date(separate_date):
    temp=set()
    for i in separate_date:
        temp=temp|set(separate_date[i])
    return temp

bbstable_dead_foxconn_date_combine=combine_date(bbstable_dead_foxconn_date)
bbstable_dead_uni_date_combine=combine_date(bbstable_dead_uni_date)
bbstable_dead_TSMC_date_combine=combine_date(bbstable_dead_TSMC_date)

forumtable_dead_foxconn_date_combine=combine_date(forumtable_dead_foxconn_date)
forumtable_dead_uni_date_combine=combine_date(forumtable_dead_uni_date)
forumtable_dead_TSMC_date_combine=combine_date(forumtable_dead_TSMC_date)

newstable_dead_foxconn_date_combine=combine_date(newstable_dead_foxconn_date)
newstable_dead_uni_date_combine=combine_date(newstable_dead_uni_date)
newstable_dead_TSMC_date_combine=combine_date(newstable_dead_TSMC_date)

#合併所有dead_公司的新聞
dead_foxconn=pd.concat([get_data(bbs_table, list(bbstable_dead_foxconn_date_combine)), get_data(forum_table, list(forumtable_dead_foxconn_date_combine)), get_data(news_table, list(newstable_dead_foxconn_date_combine))])

dead_uni=pd.concat([get_data(bbs_table, list(bbstable_dead_uni_date_combine)), get_data(forum_table, list(forumtable_dead_uni_date_combine)), get_data(news_table, list(newstable_dead_uni_date_combine))])

dead_TSMC=pd.concat([get_data(bbs_table, list(bbstable_dead_TSMC_date_combine)), get_data(forum_table, list(forumtable_dead_TSMC_date_combine)), get_data(news_table, list(newstable_dead_TSMC_date_combine))])

dead_foxconn.to_csv("/Users/leepinghsun/Desktop/bda2019_dataset/dead_foxconn.csv")
dead_uni.to_csv("/Users/leepinghsun/Desktop/bda2019_dataset/dead_uni.csv")
dead_TSMC.to_csv("/Users/leepinghsun/Desktop/bda2019_dataset/dead_TSMC.csv")

bbstable_rise_foxconn_date=find_date_index(golden_cross_date["foxconn"],bbs_table, idx["bbstable_foxconn"])
bbstable_rise_uni_date=find_date_index(golden_cross_date["uni"],bbs_table, idx["bbstable_uni"])
bbstable_rise_TSMC_date=find_date_index(golden_cross_date["TSMC"],bbs_table, idx["bbstable_TSMC"])

forumtable_rise_foxconn_date=find_date_index(golden_cross_date["foxconn"],forum_table, idx["forumtable_foxconn"])
forumtable_rise_uni_date=find_date_index(golden_cross_date["uni"],forum_table, idx["forumtable_uni"])
forumtable_rise_TSMC_date=find_date_index(golden_cross_date["TSMC"],forum_table, idx["forumtable_TSMC"])

newstable_rise_foxconn_date=find_date_index(golden_cross_date["foxconn"],news_table, idx["forumtable_foxconn"])
newstable_rise_uni_date=find_date_index(golden_cross_date["uni"],news_table, idx["forumtable_uni"])
newstable_rise_TSMC_date=find_date_index(golden_cross_date["TSMC"],news_table, idx["forumtable_TSMC"])

bbstable_rise_foxconn_date_combine=combine_date(bbstable_rise_foxconn_date)
bbstable_rise_uni_date_combine=combine_date(bbstable_rise_uni_date)
bbstable_rise_TSMC_date_combine=combine_date(bbstable_rise_TSMC_date)

forumtable_rise_foxconn_date_combine=combine_date(forumtable_rise_foxconn_date)
forumtable_rise_uni_date_combine=combine_date(forumtable_rise_uni_date)
forumtable_rise_TSMC_date_combine=combine_date(forumtable_rise_TSMC_date)

newstable_rise_foxconn_date_combine=combine_date(newstable_rise_foxconn_date)
newstable_rise_uni_date_combine=combine_date(newstable_rise_uni_date)
newstable_rise_TSMC_date_combine=combine_date(newstable_rise_TSMC_date)

#合併所有rise_公司的新聞
rise_foxconn=pd.concat([get_data(bbs_table, list(bbstable_rise_foxconn_date_combine)), get_data(forum_table, list(forumtable_rise_foxconn_date_combine)), get_data(news_table, list(newstable_rise_foxconn_date_combine))])
rise_uni=pd.concat([get_data(bbs_table, list(bbstable_rise_uni_date_combine)), get_data(forum_table, list(forumtable_rise_uni_date_combine)), get_data(news_table, list(newstable_rise_uni_date_combine))])
rise_TSMC=pd.concat([get_data(bbs_table, list(bbstable_rise_TSMC_date_combine)), get_data(forum_table, list(forumtable_rise_TSMC_date_combine)), get_data(news_table, list(newstable_rise_TSMC_date_combine))])

rise_foxconn.to_csv("/Users/leepinghsun/Desktop/bda2019_dataset/rise_foxconn.csv")
rise_uni.to_csv("/Users/leepinghsun/Desktop/bda2019_dataset/rise_uni.csv")
rise_TSMC.to_csv("/Users/leepinghsun/Desktop/bda2019_dataset/rise_TSMC.csv")


# In[31]:


#全部合併的，沒有分公司
bbs_dead_idx=set()
for i in bbstable_dead_foxconn_date:
    bbs_dead_idx=bbs_dead_idx|set(bbstable_dead_foxconn_date[i])
for i in bbstable_dead_uni_date:
    bbs_dead_idx=bbs_dead_idx|set(bbstable_dead_uni_date[i])
for i in bbstable_dead_TSMC_date:
    bbs_dead_idx=bbs_dead_idx|set(bbstable_dead_TSMC_date[i])
print(len(bbs_dead_idx))
bbs_dead_idx=list(bbs_dead_idx)
bbs_dead=get_data(bbs_table, bbs_dead_idx)


# In[32]:


forum_dead_idx=set()
for i in forumtable_dead_foxconn_date:
    forum_dead_idx=forum_dead_idx|set(forumtable_dead_foxconn_date[i])
for i in forumtable_dead_uni_date:
    forum_dead_idx=forum_dead_idx|set(forumtable_dead_uni_date[i])
for i in forumtable_dead_TSMC_date:
    forum_dead_idx=forum_dead_idx|set(forumtable_dead_TSMC_date[i])
print(len(forum_dead_idx))
forum_dead_idx=list(forum_dead_idx)
forum_dead=get_data(forum_table, forum_dead_idx)


# In[33]:


news_dead_idx=set()
for i in newstable_dead_foxconn_date:
    news_dead_idx=news_dead_idx|set(newstable_dead_foxconn_date[i])
for i in newstable_dead_uni_date:
    news_dead_idx=news_dead_idx|set(newstable_dead_uni_date[i])
for i in newstable_dead_TSMC_date:
    news_dead_idx=news_dead_idx|set(newstable_dead_TSMC_date[i])
print(len(news_dead_idx))
news_dead_idx=list(news_dead_idx)
news_dead=get_data(news_table, news_dead_idx)


# In[17]:


dead=pd.concat([news_dead,forum_dead, bbs_dead])


# In[26]:


dead.to_csv("/Users/leepinghsun/Desktop/bda2019_dataset/dead_news.csv")


# In[20]:


bbs_rise_idx=set()
for i in bbstable_rise_foxconn_date:
    bbs_rise_idx=bbs_rise_idx|set(bbstable_rise_foxconn_date[i])
for i in bbstable_rise_uni_date:
    bbs_rise_idx=bbs_rise_idx|set(bbstable_rise_uni_date[i])
for i in bbstable_rise_TSMC_date:
    bbs_rise_idx=bbs_rise_idx|set(bbstable_rise_TSMC_date[i])
print(len(bbs_rise_idx))
bbs_rise_idx=list(bbs_rise_idx)
bbs_rise=get_data(bbs_table, bbs_rise_idx)


# In[21]:


forum_rise_idx=set()
for i in forumtable_rise_foxconn_date:
    forum_rise_idx=forum_rise_idx|set(forumtable_rise_foxconn_date[i])
for i in forumtable_rise_uni_date:
    forum_rise_idx=forum_rise_idx|set(forumtable_rise_uni_date[i])
for i in forumtable_rise_TSMC_date:
    forum_rise_idx=forum_rise_idx|set(forumtable_rise_TSMC_date[i])
print(len(forum_rise_idx))
forum_rise_idx=list(forum_rise_idx)
forum_rise=get_data(forum_table, forum_rise_idx)


# In[22]:


news_rise_idx=set()
for i in newstable_rise_foxconn_date:
    news_rise_idx=news_rise_idx|set(newstable_rise_foxconn_date[i])
for i in newstable_rise_uni_date:
    news_rise_idx=news_rise_idx|set(newstable_rise_uni_date[i])
for i in newstable_rise_TSMC_date:
    news_rise_idx=news_rise_idx|set(newstable_rise_TSMC_date[i])
print(len(news_rise_idx))
news_rise_idx=list(news_rise_idx)
news_rise=get_data(news_table, news_rise_idx)


# In[23]:


rise=pd.concat([news_rise,forum_rise, bbs_rise])


# In[25]:


rise.to_csv("/Users/leepinghsun/Desktop/bda2019_dataset/rise_news.csv")


# In[24]:


len(rise)