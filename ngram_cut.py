import pandas as pd
import numpy as np
import xlwt
import sys
import time
from progressbar import *


# 交換dictionary的key與value
def invert_dict(d):
    inv = dict()
    for key in d:
        # print(d[key])
        val = d[key][0]
        if val not in inv:
            inv[val] = [key]
        else:
            inv[val].append(key)
    print("invert completed")
    return inv


#  將數據寫入新文件
def data_write(file_name, vol, tf, df, i):
    # 將數據寫入第 i 行，第 j 列
    sheet1.write(i, 0, vol)
    sheet1.write(i, 1, tf)
    sheet1.write(i, 2, df)

    # 保存文件
    f.save(file_name)


def punc_in_word(string, first, last, punc):
    for i in range(first, last + 1):
        if (string[i] in punc):
            return True
    return False


def dosomework():
    time.sleep(0.01)


pbar = ProgressBar().start()

sheet = ["Foxconn", "Uni"]

for k in range(len(sheet)):
    # 讀取excel檔
    df = pd.read_excel("/Users/leepinghsun/Desktop/bda2019_all_bbs.xlsx", sheet[k])
    df = pd.DataFrame(df)

    # 創建excel檔
    file_name = "bbs_all_" + sheet[k] + ".xls"
    f = xlwt.Workbook(encoding='utf-8')
    # 創建sheet
    sheet1 = f.add_sheet(sheet[k])
    sheet1.write(0, 0, "詞")
    sheet1.write(0, 1, "tf")
    sheet1.write(0, 2, "df")
    # 打開檔案
    # file_name = "forum_output.xlsx"
    # wb = load_workbook(file_name)

    # # 創建sheet
    # wb.create_sheet(sheet[k])

    # sheets = wb.sheetnames

    # wb[sheets[k]].cell(row = 1, column = 1).value = "詞"
    # wb[sheets[k]].cell(row = 1, column = 2).value = "tf"
    # wb[sheets[k]].cell(row = 1, column = 3).value = "df"
    # wb.save(file_name)

    # 將標題與內容的文字存入csv
    csv = []
    for index, row in df.iterrows():
        csv.append(str(row['title']) + str(row['title']) + str(row['content']) + '    ')
    csv.append("END")

    # 中文斷詞
    stops = []
    with open('/Users/leepinghsun/Desktop/stops.txt', 'r', encoding='utf8') as f1:
        stops = f1.read().split('\n')

    countTf = dict()
    countDf = dict()
    punc = ' \'"?;,.!:()[]%{}\n\r\t=#+/\\><-~＿－—─▇▇▋：，。「」　…！『』（）、？***“”|abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWKYZ1234567890１２３４５６７８９０'

    # n-gram
    n = 1
    index = 0

    while True:
        if csv[index] == "END":
            break
        else:
            firstLetter = 0
            while firstLetter < (len(csv[index]) - 4):
                lastLetter = firstLetter + n
                if (punc_in_word(csv[index], firstLetter, lastLetter, punc)) or (
                        csv[index][firstLetter:lastLetter + 1] in stops):
                    if n <= 2:
                        n += 1
                    else:
                        firstLetter += 1
                        n = 1
                else:
                    word = csv[index][firstLetter: lastLetter + 1]
                    if word not in countTf:
                        countTf[word] = [1, False]
                        countDf[word] = 1
                    else:
                        countTf[word][0] += 1
                        if (countTf[word][1] == True):
                            countDf[word] += 1
                            countTf[word][1] = False
                    if n <= 2:
                        n += 1
                    else:
                        firstLetter += 1
                        n = 1
            # 新的一篇新聞，df全部重算
            for key, value in countTf.items():
                value[1] = True
            index += 1

        pbar.update(int(index / (len(csv) - 1) * 100))
        dosomework()
    pbar.finish()
    print("count completed")

    inverted_tf = invert_dict(countTf)
    counter = 0
    keyList_tf = inverted_tf.keys()
    for key in sorted(keyList_tf, reverse=True):
        inverted_tf[key].sort()
        # 輸出前1000筆
        if counter >= 1000:
            break
        else:
            for i in range(len(inverted_tf[key])):
                if counter >= 1000:
                    break
                else:
                    df = ''
                    for j in countDf.keys():
                        if j == inverted_tf[key][i]:
                            df = countDf[j]
                            break
                    data_write(file_name, inverted_tf[key][i], key, df, counter + 1)
                    counter += 1

    print("completed")