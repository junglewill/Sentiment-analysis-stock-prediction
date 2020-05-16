import csv
import pandas as pd
import datetime
import re

#  Open two files, the news and the date excel file, the latter contains the date target stock prices rise or decline for more than 1%
#  Because the dataset is huge, to prevent from time lapsing, change the "forum.csv" name everytime, change to "news.csv", for example 
infile = open("/Users/leepinghsun/Desktop/bda2019_dataset/forum.csv", 'r', encoding='utf-8')
csv1 = csv.DictReader(infile)
cname1 = csv1.fieldnames
date_infile = open('/Users/leepinghsun/Desktop/date.csv', 'r', encoding='utf-8')
date_csv1 = csv.DictReader(date_infile)
date_cname1 = date_csv1.fieldnames   # type(data) is str

time_TSMC = []
time_foxconn = []
time_uni = []
for aline in date_csv1:  # TSMC, Foxconn, and Uni match the column, 1900/1/0 represent the date excel print as 0
    if aline[date_cname1[7]] != '1900/1/0':
        list1 = aline[date_cname1[7]].split('/')
        date1 = datetime.datetime(int(list1[0]), int(list1[1]), int(list1[2]))
        time_TSMC.append(date1.strftime('%Y/%-m/%d'))
        day1 = date1.weekday()
        if day1 == 4:
            sat1 = date1 + datetime.timedelta(days=1)
            sun1 = date1 + datetime.timedelta(days=2)
            time_TSMC.append(sat1.strftime('%Y/%-m/%d'))
            time_TSMC.append(sun1.strftime('%Y/%-m/%d'))
    if aline[date_cname1[9]] != '1900/1/0':
        list2 = aline[date_cname1[9]].split('/')
        date2 = datetime.datetime(int(list2[0]), int(list2[1]), int(list2[2]))
        time_foxconn.append(date2.strftime('%Y/%-m/%d'))
        day2 = date2.weekday()
        if day2 == 4:
            sat2 = date2 + datetime.timedelta(days=1)
            sun2 = date2 + datetime.timedelta(days=2)
            time_foxconn.append(sat2.strftime('%Y/%-m/%d'))
            time_foxconn.append(sun2.strftime('%Y/%-m/%d'))
    if aline[date_cname1[10]] != '1900/1/0':
        list3 = aline[date_cname1[10]].split('/')
        date3 = datetime.datetime(int(list3[0]), int(list3[1]), int(list3[2]))
        time_uni.append(date3.strftime('%Y/%-m/%d'))
        day3 = date3.weekday()
        if day3 == 4:
            sat3 = date3 + datetime.timedelta(days=1)
            sun3 = date3 + datetime.timedelta(days=2)
            time_uni.append(sat3.strftime('%Y/%-m/%d'))
            time_uni.append(sun3.strftime('%Y/%-m/%d'))

# remove the repetitions
time_TSMC_no = []
time_foxconn_no = []
time_uni_no = []
for i in range(len(time_TSMC)):
    if time_TSMC[i] not in time_TSMC_no:
        time_TSMC_no.append(time_TSMC[i])
for i in range(len(time_foxconn)):
    if time_foxconn[i] not in time_foxconn_no:
        time_foxconn_no.append(time_foxconn[i])
for i in range(len(time_uni)):
    if time_uni[i] not in time_uni_no:
        time_uni_no.append(time_uni[i])

list_content = []
list_id = []
list_time = []
list_type = []
list_area_name = []
list_title = []
dict = {}

key_TSMC = ["台積電", "張忠謀", "劉德音", "魏哲家", "晶圓", "代工", "奈米", "製程", "半導體", "晶片", "積體", "電路"]
key_foxconn = ["鴻海", "夏普", "台積電", "指數", "外資", "法人", "供應鏈", "和碩", "友達", "日月光"]
key_uni =["統一", "零售", "物流", "食品", "加工", "棒球", "味全", "超商", "兄弟", "星巴克", "百貨"]


for aline in csv1:
    if aline[cname1[4]] not in dict:
        dict[aline[cname1[4]]] = aline[cname1[4]]

#  Remove the character error that would happen while using openxlrx in ASCI code
illegal_character = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

# Use a for loop to screen through if the date and keywords in the str of date and content
for aline in csv1:
    # for i in range(len(time_uni_no)):
    #     if time_uni_no[i] in aline[cname1[5]]:
    aline[cname1[8]] = illegal_character.sub(r'', aline[cname1[8]])
    x = aline[cname1[5]][0:4]
    if x == "2016" or x == "2017": 
        for j in key_uni: # to create a excel file just for company Uni-President featured news
            if j in aline[cname1[8]] and aline[cname1[8]] not in list_content:
                list_time.append(aline[cname1[5]])
                list_id.append(aline[cname1[0]])
                list_area_name.append(aline[cname1[3]])
                list_title.append(aline[cname1[6]])
                list_content.append(aline[cname1[8]])
                list_type.append(aline[cname1[1]])


# Create a DataFrame, and use to.excel to export as an excel file
df = pd.DataFrame({'id': list_id,
                   'type': list_type,
                   's_area_name': list_area_name,
                   'post time': list_time,
                   'title': list_title,
                   'content': list_content})

#  Because the dataset is huge, to prevent from time lapsing, change the "forum.csv" name everytime, change to "news.csv", for example 
df.to_excel('/Users/leepinghsun/Desktop/bda2019_mid_project_forum2.xlsx', 'Uni', index=False, header=True)


