import os
import numpy as np
import pandas as pd
import copy
data=[]
def Init():
    '''
    初始化，生成树,设置阈值，初始化要匿名的属性值
    :return: 所有数据元祖，阈值，所有属性的树
    '''

    #第一步：读取数据，生成元组
    path = os.path.abspath('..')  # 表示当前所处的文件夹上一级文件夹
    data_path = path + '\\data\\data.txt'
    data_file = open(data_path, 'r')
    lines = data_file.readlines()
    for line in lines:
        i = line[:-1].split(',')
        data.append(i)
    return data
Init()
print(data)
Dr = 0
def DisRate(data):
    column = []
    column = [data[i][j] for j in range(7) for i in range(len(data))]
    # 所有数据按属性顺序导入列表column并备份
    print(column)
    list_1 = []
    for y in range(7):
        list_0 = [x[y] for x in data]
        list_1.append(list_0)
    #导出按列排序的数据列表
    Dr = [set(list_1[i]) for i in range(7)]
    res_DR = [len(Dr[i]) for i in range(7)]
    DR = max(res_DR)
    #返回最大识别率DR
    return DR
def original_entropy(data):
    entropy =
def GetAttrLoss(attr,data):
    origin = GetNewLoss_2(data)
    for i in range(len(data)):
        data[i] = data[i][:] #再次拷贝子列表数据

    depth = 0
    for i in range(len(data)):
        tmp_attribute = climb(Trees[attr], data[i][attr])  # 得到父节点
        data[i][attr] = tmp_attribute  # 更新匿名属性
        depth = depth + Trees[attr].depth(tmp_attribute)

    depth = depth / len(data)
    after = GetNewLoss_2(data)
    ret = ((origin - after) / origin)
    print("属性列"+str(attr+1)+" 泛化至深度"+str(depth)+" 损失:"+str(ret))
    return ret,depth