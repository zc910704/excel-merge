#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import re
import os

result_list =[]


BASE_DIR = os.getcwd()


def verify_file(path):
    reg = re.compile('分部分项')
    if reg.search(path):
    # if path.find('分部分项') + 1 :
        return True
    return False


def readTable(filePath):
    data = pd.read_excel(filePath)
    df = pd.DataFrame(columns=data.iloc[1])
    data.columns = data.iloc[1]
    for index,row in data.iterrows():
        if re.match('\d+',str(row['项目编码'])):
            df = df.append(row)
    return df.loc[:, [column for column in df.columns if str(column) != 'nan']]


def traverse(BASE_DIR):
    files = os.listdir(BASE_DIR)
    for file in files:
        tmp_path = os.path.join(BASE_DIR, file)
        if not os.path.isdir(tmp_path):
            if verify_file(tmp_path):
                print('file found')
                res = readTable(tmp_path)
                result_list.append(res)
        else:
            traverse(tmp_path)

traverse(BASE_DIR)

df = pd.concat(result_list).sort_values(by="项目编码")

df.to_excel('./out.xls')
