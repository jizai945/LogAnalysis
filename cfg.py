# -*- coding: utf-8 -*-
# 读取配置文件

from configparser import ConfigParser

class MYINI:
    '''读取ini中的事件配置'''
    def __init__(self, ini_file="./ini/test.ini"):
        self.cfg = ConfigParser()
        # 读取文件内容
        self.cfg.read(ini_file, encoding="utf-8")

        # 获取所有的section
        self.sections = self.cfg.sections()   

        # 类内变量
        self.result = False

    # 获取所有sections片段(元组的方式返回)
    def getAllSections(self):
        return self.sections

    # 获取section片段下的配置(字典的方式返回)
    def getCfgBySection(self, section='none'):
        try:
            return dict(self.cfg.items(section))
        except:
            return {}

    # 打印片段
    def print_sections(self):
        print(self.sections)  # 返回list

    # 打印子配置
    def print_cfg(self):
        for se in self.sections:
            # cfg.items()返回list，元素为tuple
            db_cfg = dict(self.cfg.items(se))
            # 打印参数
            print(db_cfg)
    
    # 通过一行can命令字符串获取当前的事件
    def getEventByCanStr(self, can_cmd=''):
        # 判断命令是否为空
        if len(can_cmd) == 0:
            return '无'

        # if (can_cmd[:4] == '0x16'):
        #     return '固件升级事件'
        # elif (can_cmd[:4] == '0x73'):
        #     return '充电信息'

        for se in self.sections:
            self.result = False
            cfg = self.getCfgBySection(se)
            
            # 遍历 b0 ~ b7
            for i in range(0, 8):
                
                if 'b'+str(i) in cfg :

                    # 有配置则先设置结果为错误
                    self.result = False
                    # 转换成列表
                    cfg_list = eval(cfg['b'+str(i)])

                    # 遍历列表中的数据，存在即代表改字节配置判断ok
                    for li in cfg_list:
                        if(li == int(can_cmd[i*5: i*5+4], 16)):
                            self.result = True
                            break
            
            # 有事件判断成功
            if (self.result == True):
                return se

            # 否则循环判断下一个事件
            


        return '无'
             

        

if __name__ == '__main__':
    ini_file = "./ini/test.ini"

    myini = MYINI(ini_file)
    myini.print_cfg()
    myini.print_sections()

    # print(myini.getAllSections())
    # event = myini.getCfgBySection('充电事件')
    
    # mylist = ['b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7']
    # for li in mylist:
    #     if (li in event):
    #         print(event[li])
    #     else:
    #         print(f'{li} is not in event')
    # print(123)


    event = myini.getCfgBySection('雾化事件')
    print(event['b1'])
    print(eval(event['b1']))
    print(type(eval(event['b1'])))

    print(event['b0'])
    print(eval(event['b0']))
    print(type(eval(event['b0'])))







