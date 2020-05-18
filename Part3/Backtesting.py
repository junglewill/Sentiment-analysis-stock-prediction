import math
import pandas as pd
import numpy as np
import datetime

stock_all = pd.read_csv('/Users/yesno6713no/Desktop/大數據與商業分析/期中資料/stock_data_2018.csv')
stock_2018 = pd.read_csv('/Users/yesno6713no/Desktop/大數據與商業分析/期中資料/2018_鴻海_stock.csv')
predict_2018 = pd.read_csv('/Users/yesno6713no/Desktop/大數據與商業分析/期中資料/foxconn_forest_predict_result.csv')
price = list(stock_2018['price'])
date_happen = list(stock_2018['date'])
predict_time = list(predict_2018['post_time'])
predict_result = list(predict_2018['predict_results'])

def change_price(price):
    change = []
    for i in range(len(price)-1):
        number = (price[i+1]-price[i])/price[i]
        change.append(number)
    return change
change = change_price(price)

def result_symbol(change):
    result = []
    for number in change:
        if number >= 0.01:
            result.append('U')
        elif number <= -0.01:
            result.append('F')
        else:
            result.append('N')
    return result
    
change_result = result_symbol(change)

actual_result = {}
predict_result_compare = {}
for i in range(len(date_happen)-1):
    actual_result[date_happen[i+1]] = change_result[i]

for x in range(len(predict_time)):
    predict_result_compare[predict_time[x]] = predict_result[x].upper()

tp_result = 0
fp_result = 0
tn_result = 0
fn_result = 0
for time in range(len(date_happen)-1):
    date = date_happen[time+1]
    result = actual_result[date]
    decision = predict_result_compare[date]
    if decision == 'U' or decision == 'F':
        if decision == result:
            tp_result += 1
        elif decision != result:
            fp_result += 1
    else:
        if result == 'N':
            tn_result +=1
        else:
            fn_result +=1

def accuaracy(tp,fp,fn,tn):
    A = (tp+tn)/(tp+fp+fn+tn)
    P = tp/(tp+fp)
    R = tp/(tp+fn)
    F1 = 2*P*R/(P+R)
    return A,P,R,F1

result_final = accuaracy(tp_result,fp_result,fn_result,tn_result)

print('accuaracy :',result_final[0],'precision:',result_final[1],'recall:',result_final[2],'F1:',result_final[3])

