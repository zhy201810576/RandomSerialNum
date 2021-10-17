#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''  
---------------------------------------
 # @Project    : 随机生成序列号
 # @File       : view.py
 # @Author     : GrayZhao
 # @Date       : 2021/10/15 15:43
 # @Version    : 1.0.0-alpha
 # @Desciption : 视图主体函数
---------------------------------------
'''
from PySide2.QtWidgets import QApplication, QCompleter, QTableWidgetItem, QInputDialog, QLineEdit, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, QObject, Signal
import sys
import os
from threading import Thread
from controller import RandomNumCore


# 自定义信号源对象类型，一定要继承自 QObject
class MySignals(QObject):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    # 单元格文本
    cellText = Signal(str, int)
    # 还可以定义其他种类的信号
    # 单元格数量
    cellNum = Signal(int)
    # 状态栏消息
    statusMsg = Signal(str)
    # 弹出提示窗口
    promptMsg = Signal()
    # 弹出警告窗口
    errorMsg = Signal()
    # 弹出输入窗口
    inputData = Signal(list)
    # 自锁信号
    autoLock = Signal()


class MainWindow:
    def __init__(self):
        # 从文件中加载UI定义
        self.ui = QUiLoader().load(os.path.join(os.getcwd(), "main.ui"))
        # 设置窗口图标
        self.ui.setWindowIcon(QIcon(os.path.join(os.getcwd(), "logo.png")))
        # 实例化 MySignals
        self.ms = MySignals()
        # 设置输入框提示文本
        self.ui.prefixLineEdit.setPlaceholderText('请在此输入序列号前缀')
        # 设置输入框提示文本
        self.ui.specialIdLineEdit.setPlaceholderText('多个请用‘,’分隔')
        # 绑定程序执行
        self.ui.startButton.clicked.connect(self.createTask)
        # 实例化随机数生成核心
        self.randomNumCore = RandomNumCore()
        # 设置表格列宽
        self.ui.tableWidget.setColumnWidth(0, 282)
        # 获取保存的历史数据
        self.getSaveData()
        # 生成自动补全提示
        self.ui.prefixLineEdit.textChanged.connect(self.automatic)
        # 用户输入的数据
        self.inputSpecialId = str()  # type: str
        # 绑定信号与槽
        self.ms.cellNum.connect(self._setCellNum)  # 绑定单元格数量信号
        self.ms.cellText.connect(self._setCellText)  # 绑定单元格文本信号
        self.ms.statusMsg.connect(self._sendStatusMsg)  # 绑定状态栏信号
        self.ms.promptMsg.connect(self._promptMessageBox)  # 绑定提示弹窗信号
        self.ms.errorMsg.connect(self._errorMessageBox)  # 绑定错误弹窗信号
        self.ms.inputData.connect(self._inputDialog)  # 绑定输入弹窗信号
        self.ms.autoLock.connect(self._antiMisOperation)  # 绑定按钮控件信号
        # 提示语
        self.sendStatusMsg("准备就绪...")

    def setCellNum(self, num: int):
        """
        设置单元格数量(触发器)
        :param num: 需要设置的单元格数量
        """
        self.ms.cellNum.emit(num)

    def _setCellNum(self, num: int):
        """
        设置单元格数量(执行函数)
        :param num: 需要设置的单元格数量
        """
        self.ui.tableWidget.setRowCount(num)

    def setCellText(self, text: str, row: int):
        """
        设置单元格内容文本(触发器)
        :param text: 内容文本
        :param row: 在第几行设置文本
        """
        self.ms.cellText.emit(text, row)

    def _setCellText(self, text: str, row: int):
        """
        设置单元格内容文本(执行函数)
        :param text: 内容文本
        :param row: 在第几行设置文本
        """
        item = QTableWidgetItem()
        item.setText(text)
        item.setFlags(Qt.ItemIsEnabled)  # 参数名字段不允许修改
        self.ui.tableWidget.setItem(row, 0, item)

    def sendStatusMsg(self, msg: str):
        """
        发送状态消息(触发器)
        :param msg: 消息体
        """
        self.ms.statusMsg.emit(msg)

    def _sendStatusMsg(self, msg: str):
        """
        发送状态消息(执行函数)
        :param msg: 消息体
        """
        self.ui.statusbar.showMessage(msg)

    def getRandomNum(self, idRow: int, digits: int):
        """
        获取随机序列号
        :param idRow: 一次性生成多少位序列号
        :param digits: 生成序列号的位数
        """
        self.randomNumCore.randomNum(idRow=idRow, digits=digits)

    def automatic(self):
        """
        自动补全显示
        """
        prefixList = self.randomNumCore.getAutomatic()
        completer = QCompleter(prefixList)
        self.ui.prefixLineEdit.setCompleter(completer)

    def getSaveData(self):
        """
        获取储存的数据
        """
        self.randomNumCore.readSave()

    def putSaveData(self, prefix: str):
        """
        保存当前序列号数据
        :param prefix: 序列号前缀
        """
        self.randomNumCore.writerSave(prefix)

    def exportSerialNum(self, prefix: str):
        """
        导出生成的随机序列号
        :param prefix: 序列号前缀
        """
        self.randomNumCore.exportSerialNumToCSV(prefix)

    def clearTableWidget(self):
        """
        清除表格窗口中的数据
        """
        self.ui.tableWidget.clearContents()

    def clearRandomNumCore(self):
        """
        清理随机序列号核心逻辑产生的内存
        """
        self.randomNumCore.clearRAM()

    def _promptMessageBox(self):
        """
        弹窗提示(执行函数)
        """
        QMessageBox.information(self.ui, "序列号导出完成", "请前往程序所在文件目录下查看")

    def promptMessageBox(self):
        """
        弹窗提示(触发器)
        """
        self.ms.promptMsg.emit()

    def errorMessageBox(self):
        """
        警告弹窗(触发器)
        """
        self.ms.errorMsg.emit()

    def _errorMessageBox(self):
        """
        警告弹窗(执行函数)
        """
        QMessageBox.critical(self.ui, "操作错误", "序列号位数与生成个数不能为空!!!")

    def inputDialog(self, errorId: list):
        """
        输入弹窗(触发器)
        :param errorId 用户输入的有误序列号
        """
        self.ms.inputData.emit(errorId)

    def _inputDialog(self, errorId: list):
        """
        输入弹窗(执行函数)
        :param errorId 用户输入的有误序列号
        """
        specialId, okPressed = QInputDialog.getText(self.ui,
                                                    "输入有误",
                                                    ",".join(errorId) + "\n以上序列号的输入有误，请重新输入",
                                                    QLineEdit.Normal,
                                                    "")
        if specialId.strip() and okPressed:
            self.inputSpecialId = specialId

    def _antiMisOperation(self):
        """
        改变startButton的可用性，防止用户误操作(执行函数)
        """
        if self.ui.startButton.isEnabled():
            self.ui.startButton.setEnabled(False)
        else:
            self.ui.startButton.setEnabled(True)

    def antiMisOperation(self):
        """
        改变startButton的可用性，防止用户误操作(触发器)
        """
        self.ms.autoLock.emit()

    def unrepeated_1(self, prefix: str):
        """
        第一次去重，去除以前保存的序列号
        :param prefix: 序列号前缀
        """
        self.randomNumCore.removeSavedSerialNum(prefix)

    def unrepeated_2(self, digits: int, specialId: str):
        """
        第二次去重，去除用户输入的序列号
        :param digits: 序列号位数
        :param specialId: 用户输入的序列号
        """
        while True:
            errorId = self.randomNumCore.removeUnwantedSerialNum(specialId, digits)
            if errorId:
                self.sendStatusMsg("需要排除的序列号中有个别错误")
                self.inputDialog(errorId)
                while True:
                    specialId = self.inputSpecialId
                    if specialId:
                        self.inputSpecialId = str()
                        break
            else:
                break

    def main(self):
        """
        主函数
        """
        self.antiMisOperation()  # 重置按钮状态
        self.sendStatusMsg("正在获取数据...")
        # 获取序列号位数
        digits = self.ui.digitsSpin.value()  # type: int
        # 获取生成序列号的个数
        idRow = self.ui.idRowSpin.value()  # type: int
        # 判断序列号位数与生成序列号的个数是否为空
        if digits and idRow:
            # 获取序列号前缀
            prefix = self.ui.prefixLineEdit.text()  # type: str
            # 获取用户需要去除的序列号
            specialId = self.ui.specialIdLineEdit.text()  # type: str
            self.sendStatusMsg("正在生成随机序列号...")
            self.getRandomNum(idRow, digits)  # 获取随机序列号
            self.unrepeated_1(prefix)  # 第一次去重
            # 排除用户需要去除的序列号为空
            if specialId.strip():
                self.unrepeated_2(digits, specialId)
            randomNumList = self.randomNumCore.randomNumList  # type: list
            self.clearTableWidget()  # 清理表格控件
            self.setCellNum(len(randomNumList))  # 设置表格控件的单元格行数
            for i, randomNum in enumerate(randomNumList):
                # 设置表格控件的单元格文本
                self.setCellText(prefix + str(randomNum), i)
            self.sendStatusMsg("序列号生成成功...")
            self.sendStatusMsg("正在保存序列号记录...")
            self.putSaveData(prefix)  # 保存生成的序列号数据
            self.sendStatusMsg("序列号记录保存完成...")
            self.sendStatusMsg("正在导出序列号至表格...")
            self.exportSerialNum(prefix)  # 导出生成的序列号数据
            self.sendStatusMsg("序列号导出完成...")
            self.antiMisOperation()  # 重置按钮状态
            self.clearRandomNumCore()  # 清理随机序列号生成核心所占内存
            self.promptMessageBox()  # 弹出提示窗口
            self.getSaveData()  # 获取保存的历史数据
        else:
            self.errorMessageBox()  # 弹出错误窗口
            self.antiMisOperation()  # 重置按钮状态

    def createTask(self):
        """
        创建任务线程并执行
        """
        thread = Thread(target=self.main)
        thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    stats = MainWindow()
    stats.ui.show()
    sys.exit(app.exec_())
