#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   conf.py
@Time    :   2020/07/21 19:56:17
@Author  :   waleslau 
@Version :   1.0
@Contact :   waleslau@foxmail.com
"""

# 爬取类型
# 0 : 你好污啊
# 1 : 毒鸡汤
TYPE = 0

# 爬取次数
TIMES = 10

## 是否保存到数据库
SAVE_TO_MONGO = True
# 数据库配置信息
# 连接信息，请修改为你自己的，格式为：'mongodb://user:passwd@hostname:port'
# 下面的数据库是我建立的测试用环境，随时下线
MONGO_CONNECTION_STRING = 'mongodb://admin:000000@39.107.48.220:27017'
# 数据库名字
MONGO_DB_NAME = 'nihaowua'
# 保存数据的集合的名字
MONGO_COLLECTION_NAME_WU = 'nihaowua'  # 你好污啊
MONGO_COLLECTION_NAME_DU = 'dujitang'  # 毒鸡汤