import math 
import pandas as pd
import numpy as np
from operator import itemgetter

Foxconn_up_raw_terms = pd.read_excel("./需求一/final_keywords/Foxconn_V2.xlsx", sheet_name = 'up_100_keywords')
Foxconn_down_raw_terms = pd.read_excel("./需求一/final_keywords/Foxconn_V2.xlsx", sheet_name = 'down_100_keywords')
TSMC_up_raw_terms = pd.read_excel("./需求一/final_keywords/TSMC_V2.xlsx", sheet_name = 'up_100_keywords')
TSMC_down_raw_terms = pd.read_excel("./需求一/final_keywords/TSMC_V2.xlsx", sheet_name = 'down_100_keywords')
Uni_up_raw_terms = pd.read_excel("./需求一/final_keywords/Uni_V2.xlsx", sheet_name = 'up_100_keywords')
Uni_down_raw_terms = pd.read_excel("./需求一/final_keywords/Uni_V2.xlsx", sheet_name = 'down_100_keywords')

foxconn_up_terms = list(Foxconn_up_raw_terms['term'])
foxconn_down_terms = list(Foxconn_down_raw_terms['term'])
TSMC_up_terms = list(TSMC_up_raw_terms['term'])
TSMC_down_terms = list(TSMC_down_raw_terms['term'])
uni_up_terms = list(Uni_up_raw_terms['term'])
uni_down_terms = list(Uni_down_raw_terms['term'])

tmp_up_terms = foxconn_up_terms + TSMC_up_terms + uni_up_terms
tmp_down_terms = foxconn_down_terms + TSMC_down_terms + uni_down_terms

# Combine the same keywords that appear in all three companies' keywords list
tmp_up_terms = list(set(tmp_up_terms))
tmp_down_terms = list(set(tmp_down_terms))

up_del_index = []
down_del_index = []
for i in range(len(tmp_up_terms)):
    for j in range(len(tmp_down_terms)):
        if tmp_up_terms[i] == tmp_down_terms[j]:
            up_del_index.append(i)
            down_del_index.append(j)
            break
up_del_index = sorted(up_del_index)
down_del_index = sorted(down_del_index)

# remove the keywords in both the rise and decline term list
up_terms = []
down_terms = []

i = 0
for j in range(len(tmp_up_terms)):
    if up_del_index[i] != j:
        up_terms.append(tmp_up_terms[j])
    else:
        i += 1
i = 0
for j in range(len(tmp_down_terms)):
    if down_del_index[i] != j:
        down_terms.append(tmp_down_terms[j])
    else:
        i += 1

print("總共有{}個上漲關鍵字".format(len(up_terms)))
print("總共有{}個下跌關鍵字".format(len(down_terms)))
print(up_terms)
print(down_terms)


# write into excel
df_up = pd.DataFrame(up_terms,columns = ['term'])
df_down = pd.DataFrame(down_terms,columns = ['term'])
with pd.ExcelWriter("漲跌關鍵字.xlsx") as writer:
    df_up.to_excel(writer, sheet_name="up_terms")
    df_down.to_excel(writer, sheet_name="down_terms")
