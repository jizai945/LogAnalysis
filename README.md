# LogAnalysis

## 日志分析工具

图形化展示下位机各个时间节点发生的状态，及数据信息

## 需求：

- a. 载入 apk can service 日志

- b.事件定义：例如充电事件， 固件升级事件， 电池更新事件

- c. 时间轴查找个时间节点状态， 图形化展示， 各事件简约展示在时间轴上，点击事件可获取详细信息

- d. 搜索事件（通过事件、时间， can 消息过滤）

- e. 方便扩展，新的事件支持

## 详细事件描述

### 电池信息反馈事件：

byte0 == 0x09

### 准备充电事件：

byte0 == 0x0c

### 充电状态反馈事件：

byte0 == 0x0d

### 充电信息反馈事件：

byte == 0x73

### 升级事件：

byte0 == 0x16

打包:

1. > pyinstaller main.py -Fw --hidden-import PySide2.QtXml

2. UI 文件夹放在 exe 目录下

3. ini 文件夹放在 exe 目录下



| 版本   | 说明                                                         |
| ------ | ------------------------------------------------------------ |
| V0.0.1 | 初版。实现: 1.单个日志加载 2.通过事件和时间过滤日志 3.通过ini文件加载事件的配置 |
|        |                                                              |
|        |                                                              |

