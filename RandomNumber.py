#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''  
---------------------------------------
 # @Project    : 随机生成不重复9位数字
 # @File       : RandomNumber.py
 # @Author     : Gray洋
 # @Date       : 2021/10/14 10:03
 # @Version    : 
 # @Desciption : 
---------------------------------------
'''

from typing import Dict
import random
import csv
import os
import json

jsonFile = dict()  # type: Dict[str,list]
specialId = list()
randomNum = [random.randint(100000000, 1000000000) for i in range(0, 30)]  # 获取30个随机9位数
savePath = os.path.join(os.getcwd(), "save.json")
if os.path.exists(savePath):
    with open(savePath, "r") as file:
        tempFile = file.read()
        if tempFile != "":
            jsonFile = json.loads(tempFile)
            print(f"当前已有前缀：{list(jsonFile.keys())}")
        else:
            print(f"记录数据受损！！需重新输入")
prefix = input("请输入序列号前缀：")
if prefix in jsonFile.keys():
    originId = jsonFile[prefix]
    randomNum = list(set(randomNum).difference(set(originId)))
else:
    jsonFile[prefix] = list()
opt = input("是否有需要排除的9位数[y/n]：")
if opt == "y":
    newId = input("请输入需要排除的9位数，多个用‘,’分隔：")
    while True:
        errorId = list()
        for num in newId.replace("，", ",").split(","):
            if len(num) == 9:
                specialId.append(num)
            else:
                errorId.append(num)
        if errorId:
            newId = input(f"输入的9位数有误：{errorId}\n请重新输入：")
        else:
            break
    randomNum = list(set(randomNum).difference(set(specialId)))
    idPath = os.path.join(os.getcwd(), "序列号.csv")
    rowList = list()
    with open(idPath, "w", newline="") as file:
        csvFile = csv.writer(file)
        for num in randomNum:
            rowList.append([prefix + str(num)])
        csvFile.writerows(rowList)
    jsonFile[prefix].extend(randomNum)
    with open(savePath, "w") as file:
        file.write(json.dumps(jsonFile))
elif opt == "n":
    idPath = os.path.join(os.getcwd(), "序列号.csv")
    rowList = list()
    with open(idPath, "w", newline="") as file:
        csvFile = csv.writer(file)
        for num in randomNum:
            rowList.append([prefix + str(num)])
        csvFile.writerows(rowList)
    jsonFile[prefix].extend(randomNum)
    with open(savePath, "w") as file:
        file.write(json.dumps(jsonFile))
