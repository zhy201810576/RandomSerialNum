#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''  
---------------------------------------
 # @Project    : 随机生成序列号
 # @File       : controller.py
 # @Author     : GrayZhao
 # @Date       : 2021/10/14 18:02
 # @Version    : 1.0.0-alpha
 # @Desciption : 随机序列号生成核心
---------------------------------------
'''

from typing import Dict
import random
import csv
import os
import json


class RandomNumCore(object):
    def __init__(self):
        """
        随机数生成核心逻辑类
        """
        # 记录存储格式
        self.saveFile = dict()  # type: Dict[str,list]
        # 记录前缀文件的路径
        self.savePath = os.path.join(os.getcwd(), "save.json")
        # 随机数存储容器
        self.randomNumList = list()  # type: list
        # 生成的序列号的存储路径
        self.idPath = os.path.join(os.getcwd(), "序列号.csv")

    @property
    def randomNumList(self):
        return self.__randomNumList

    @randomNumList.setter
    def randomNumList(self, value):
        self.__randomNumList = value

    @property
    def saveFile(self):
        return self.__saveFile

    @saveFile.setter
    def saveFile(self, value):
        self.__saveFile = value

    def clearRAM(self):
        """
        清理内存
        :return:
        """
        self.saveFile.clear()
        self.randomNumList.clear()

    def randomNum(self, idRow: int, digits: int):
        """
        随机生成序列号
        :param idRow: 一次性生成多少位序列号
        :param digits: 生成序列号的位数
        """
        for i in range(0, idRow):
            temp = random.randint(10**(digits - 1), 10**digits)
            self.randomNumList.append(temp)

    def getAutomatic(self) -> list:
        """
        获取用户以前输入的序列号前缀
        :return: 用户以前输入的序列号前缀
        """
        if self.saveFile:
            key = list(self.saveFile.keys())
            if "temp" in key:
                key.remove("temp")
            return key
        return list()

    def readSave(self):
        """
        读取用户以前生成的序列号
        """
        if os.path.exists(self.savePath):
            with open(self.savePath, "r") as file:
                tempFile = file.read()
                if tempFile != "":
                    self.saveFile = json.loads(tempFile)

    def writerSave(self, prefix: str):
        """
        写入Json文件
        :param prefix: 序列号前缀
        """
        preFix = self.__tempPrefix(prefix)
        self.saveFile[preFix].extend(self.randomNumList)
        with open(self.savePath, "w") as file:
            file.write(json.dumps(self.saveFile))

    def removeSavedSerialNum(self, prefix: str):
        """
        去除用户以前创建过的序列号
        :param prefix: 序列号前缀
        """
        preFix = self.__tempPrefix(prefix)
        if preFix in self.saveFile.keys():
            originId = self.saveFile[preFix]
            self.randomNumList = list(set(self.randomNumList).difference(set(originId)))
        else:
            self.saveFile[preFix] = list()

    def removeUnwantedSerialNum(self, tempID: str, digits: int) -> list:
        """
        去除用户不需要的序列号，并返回用户输入错误的序列号
        :param tempID: 用户需要去除的序列号
        :param digits: 序列号生成位数
        :return: 用户输入错误的序列号
        """
        # 需要排除的序列号
        specialId = list()
        errorId = list()
        for num in tempID.replace("，", ",").split(","):
            if len(num) == digits:
                specialId.append(num)
            else:
                errorId.append(num)
        if specialId:
            self.randomNumList = list(set(self.randomNumList).difference(set(specialId)))
        return errorId

    def exportSerialNumToCSV(self, prefix: str):
        """
        写入csv文件
        :param prefix: 序列号前缀
        """
        rowList = list()
        with open(self.idPath, "w", newline="") as file:
            csvFile = csv.writer(file)
            for num in self.randomNumList:
                if prefix.strip():
                    rowList.append([prefix + str(num)])
                else:
                    rowList.append([str(num)])
            csvFile.writerows(rowList)

    @staticmethod
    def __tempPrefix(prefix: str):
        """
        若用户输入的序列号前缀为空，将自动生成临时序列号前缀
        :param prefix: 序列号前缀
        :return: 序列号前缀
        """
        preFix = prefix.strip()
        if not preFix:
            preFix = "temp"
        return preFix
