
cls = ['age', 'workclass', 'fnlwgt',  'education', 'education-num', 'marital-status', 'occupation', 'relationship',
       'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'label']  # 数据属性
QID = ['age', 'workclass','education','marital-status','race','sex','native-country']

from time import sleep
import math
from model import *
import os
import pandas as pd
data = []
TreeDict = GetTreesDict()
k = 2

## 用于存储最终结果
result =pd.DataFrame(columns=QID)
precision = 0

def Init():
    '''
    初始化，生成树,设置阈值，初始化要匿名的属性值
    :return: 所有数据元祖，阈值，所有属性的树
    '''

    #第一步：读取数据，生成元组
    path = os.path.abspath('..')  # 表示当前所处的文件夹上一级文件夹
    data_path = path + '/data/data.csv'
    data_file = open(data_path, 'r')
    lines = data_file.readlines()
    for line in lines:
        i = line[:-1].split(',')
        data.append(i)

    return data


if __name__ == '__main__':

    #【1】初始化数据
    data = Init()
    # 【2】K值要大于等于2
    if k < 2:
        print("参数k不能小于2")
        exit()

    data_len = len(data)

    #【2】初始数据集如果小于K，则直接退出
    if data_len < k:
        print("数据总量小于匿名数量，无法满足条件")
        exit()

    raw_data = pd.DataFrame(data, columns=QID)
    tmp_data = raw_data.copy()

    print(tmp_data)


    attribute = " White"
    wrk_tree = TreeDict.get("race")

    loss = GetLoss(wrk_tree, attribute)
    print(loss)





    # k_result = Test_K_Anonymity(tmp_data, QID,k)
    # k_result = [True, True, True, True,True]
    # gen_tmp_data = final_generalize(treeDict, QID, tmp_data)
    #
    # print(gen_tmp_data)
    #
    # print(tmp_data)

    # k_result = Test_K_Anonymity(tmp_data, QID)

    ## 测试含税正确性
    # test_data = pd.DataFrame(
        # {'A': [1, 1, 1, 1, 1], 'B': [2, 2, 2, 2, 2], 'C': [3, 3, 3, 3, 3], 'D': [4, 4, 4, 4, 4], 'E': [5, 5, 4, 4, 5]})

    # K = 2
    #
    # k_result = Test_K_Anonymity(test_data, ['A', 'B', 'C', 'D','E'],K)
    # print(k_result)
    #
    # # while True:
    # #
    # #     #
    # #
    # # print(Trees)

        

