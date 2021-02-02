from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import os
import re
import time
import sys
from cfg import MYINI


class Main:
    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('./ui/main.ui')

        # 修改标题
        self.ui.setWindowTitle('log分析工具')

        # 表格模型绑定
        self.model = QStandardItemModel(0,3)
        self.model.setHorizontalHeaderLabels(['时间', '事件', 'can原始数据'])
        self.ui.tableView.setModel(self.model)
        # self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #所有列自动拉伸，充满界面
        # self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents) # 自适应宽度
        self.ui.tableView.setColumnWidth(0, 200)    
        self.ui.tableView.setColumnWidth(1, 200)   
        self.ui.tableView.setColumnWidth(2, 400)  
        # 设置表头颜色
        # self.ui.tableView.horizontalHeader().setStyleSheet("QHeaderView::section{background:red;}")
        # 设置被选中时的颜色
        self.ui.tableView.setStyleSheet("selection-background-color:lightblue;")

        # 按钮信号槽 
        self.ui.getfile_btn.clicked.connect(self.openFileDialog)
        # self.ui.clear_btn.clicked.connect(self.clearTableFunc)
        # self.ui.clear_btn.clicked.connect(self.readTable)
        # self.ui.clear_btn.clicked.connect(lambda: self.hideTable(9))        
        self.ui.filterBtn.clicked.connect(self.filterCallBackFunc)

        # 配置实例化
        self.mycfg = MYINI("./ini/test.ini")
        self.getAllEvent_and_updata()

        # 类变量
        self.cnt = 0
        self.mydict = {'无':[0,0,0]} # 字符串颜色字典表

    # 更新combobox中可以过滤的事件
    def getAllEvent_and_updata(self):
        self.ui.filterBox.clear()
        self.ui.filterBox.addItem('不过滤')

        event = self.mycfg.getAllSections()
        for ev in event:
            self.ui.filterBox.addItem(ev)

    # 选择文件弹窗
    def openFileDialog(self):

        self.ui.progressBar.setValue(0)

        # 生成文件对话框对象
        dialog = QFileDialog()
        # 设置文件过滤器，这里是任何文件，包括目录噢
        # dialog.setFileMode(QFileDialog.AnyFile)

        dialog.setNameFilters(["日志文件(*.log)"])
        # 设置显示文件的模式，这里是详细模式
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            self.file = fileNames[0]
        else:
            return

        size = os.path.getsize(self.file)
        index = 0

        with open(self.file, 'r') as f:
            self.model.removeRows(0, self.model.rowCount())
            while True:

                str = f.readline()  # 只读取一行内容

                if len(str) != 0:
                    self.cnt+=1

                    reResult = re.findall(".*\[(.*)\].*", str)
                    if reResult != [] and reResult[0][:2] == '0x':
                        tick = str[:8]
                        self.add_tableview(tick=tick, can = reResult[0])

                    index += len(str)
                    self.ui.progressBar.setValue(index/size*100.0)

                    # # 获取到text光标
                    # textCursor = self.ui.file_box.textCursor()
                    # # 滚动到底部
                    # textCursor.movePosition(textCursor.End)
                    # # 设置光标到text中去
                    # self.ui.file_box.setTextCursor(textCursor)

                    if ((self.cnt % 10000) == 0) :                       
                        self.ui.tableView.scrollToBottom() #滚动到底部
                        QApplication.processEvents()    # 实时刷新
                    
                else:
                    self.ui.tableView.scrollToBottom() #滚动到底部
                    self.ui.progressBar.setValue(100)
              
                    return


    # 添加一行表格
    def add_tableview(self, tick='0', event='无', can='55'):

        # 通过配置获取事件
        event = self.mycfg.getEventByCanStr(can)

        # 追加一行
        self.model.appendRow([QStandardItem(tick), 
                        QStandardItem(event), 
                        QStandardItem(can)])

        # 不在字典里，计算字符串颜色
        if event[0:2] not in self.mydict:             
            color = int(ascii(ord(event[0]))) + int(ascii(ord(event[1])))
            # print('color: '+str(color))
            self.mydict[event[0:2]] = [color%256, (color/100)%256, (color/1000)%256]
            # print(self.mydict[event[0:2]])

        # 修改事件的字体颜色
        self.model.item(self.model.rowCount()-1, 1).setForeground\
            (QBrush(QColor(self.mydict[event[0:2]][0], \
                self.mydict[event[0:2]][1], \
                    self.mydict[event[0:2]][2])))

    # 清空表格
    def clearTableFunc(self):
        self.model.removeRows(0, self.model.rowCount())

    # 隐藏某行
    def hideTable(self, num=0):
        if (self.cnt %2):
            # 隐藏
            self.ui.tableView.hideRow(num)
        else:
            # 显示
            self.ui.tableView.showRow(num)

        self.cnt+=1

    def readTable(self):

        print(self.model.rowCount())
        # print(self.model.item(0,0).text())
        # print(self.model.item(1,0).text())
        # print(self.model.item(1102,1).text())
        # print(self.model.item(1102,2).text())


        for i in range(0, self.model.rowCount()):
            if self.model.item(i, 1).text() == '充电信息':
                print(self.model.item(i, 0).text()+'can:' + self.model.item(i, 2).text())

        print('exit2')

    # 过滤事件
    def filterCallBackFunc(self):
        self.cnt = 0
        self.ui.progressBar.setValue(0)

        dateTime = self.ui.startTime.time()     
        tick1 = ((QTime.hour(dateTime)*60) + QTime.minute(dateTime)) *60 +QTime.second(dateTime)

        dateTime = self.ui.stopTime.time()     
        tick2 = ((QTime.hour(dateTime)*60) + QTime.minute(dateTime)) *60 +QTime.second(dateTime)

        for i in range(0, self.model.rowCount()):
            self.cnt += 1

            # 先判断左边再判断右边
            if (self.filterOneLineByTime(i, tick1, tick2) == True) and (self.filterOneLineByEvent(i) == True):
                self.ui.tableView.showRow(i)
            else:
                self.ui.tableView.hideRow(i)

            if (self.cnt % 10000 == 0):
                self.ui.progressBar.setValue(i/self.model.rowCount()*100.0)
                QApplication.processEvents()    # 实时刷新
        
        self.ui.progressBar.setValue(100)   

    # 过滤时间
    def filterTimeCallBackFunc(self):
        dateTime = self.ui.startTime.time()     
        print(f'start:{QTime.hour(dateTime)}:{QTime.minute(dateTime)}:{QTime.second(dateTime)}')
        tick1 = ((QTime.hour(dateTime)*60) + QTime.minute(dateTime)) *60 +QTime.second(dateTime)
        print(tick1)

        dateTime = self.ui.stopTime.time()     
        print(f'stop:{QTime.hour(dateTime)}:{QTime.minute(dateTime)}:{QTime.second(dateTime)}')
        tick2 = ((QTime.hour(dateTime)*60) + QTime.minute(dateTime)) *60 +QTime.second(dateTime)
        print(tick2)

        step = 0
        # 需要优化成二分查找 
        for i in range(0, self.model.rowCount()):
            if step == 0:
                row_tick_text = self.model.item(i, 0).text()
                row_tick = ((int(row_tick_text[0:2])*60) + int(row_tick_text[3:5]))*60+int(row_tick_text[6:8])
                if (tick1 <= row_tick):
                    print(f'{i}: {row_tick_text}')
                    step = 1
                    continue
            if step == 1:
                row_tick_text = self.model.item(i, 0).text()
                row_tick = ((int(row_tick_text[0:2])*60) + int(row_tick_text[3:5]))*60+int(row_tick_text[6:8])
                if (tick2 < row_tick):
                    print(f'{i}: {row_tick_text}')
                    return

    # 通过事件判断当前行是否需要保留
    # 入参：行号
    # 出参：True保留 / False过滤掉
    def filterOneLineByEvent(self, line = 0):
        # 事件过滤勾选框是否勾选
        if self.ui.eventCheckBox.checkState():
            if self.ui.filterBox.currentText() == '不过滤':
                return True
            if (self.ui.filterBox.currentText() != self.model.item(line, 1).text()):
                return False
            else:
                return True
        else:
            return True

    # 通过始末时间判断当前行是否需要过滤掉
    # 入参：行号, 起始时间 ， 终止时间
    # 出参：True保留 / False过滤掉
    def filterOneLineByTime(self, line = 0, start=0, stop=0):
        # 时间过滤勾选框是否勾选
        if self.ui.eventCheckBox.checkState():

            row_tick_text = self.model.item(line, 0).text()
            row_tick = ((int(row_tick_text[0:2])*60) + int(row_tick_text[3:5]))*60+int(row_tick_text[6:8])

            if start <= stop:
    
                if start <= row_tick and stop >= row_tick:
                    return True
                else:
                    return False 

            else:

                if start <= row_tick or stop >= row_tick:
                    return True
                else:
                    return False 
        else:
            return True



if __name__ == '__main__':
    
    app = QApplication([])
    
    try :
        main = Main()
        main.ui.show()
        app.exec_()
    except Exception as e:
        app.quit()
        msg_box = QMessageBox(QMessageBox.Critical, 'error', str(e))
        app.exit(msg_box.exec_())
        app.exec_()
