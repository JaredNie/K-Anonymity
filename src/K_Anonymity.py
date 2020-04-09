'''

>50K, <=50K.

age: continuous.
workclass: Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.
fnlwgt: continuous.
education: Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool.
education-num: continuous.
marital-status: Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse.
occupation: Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces.
relationship: Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried.
race: White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black.
sex: Female, Male.
capital-gain: continuous.
capital-loss: continuous.
hours-per-week: continuous.
native-country: United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands.
'''

cls = ['age', 'workclass', 'fnlwgt',  'education', 'education-num', 'marital-status', 'occupation', 'relationship', 
       'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'label']  # 数据属性

from time import sleep
import math
from model import *
import os
data=[]
Trees = GetTrees()   #保存属性的树
k = 2

def Init():
    '''
    初始化，生成树,设置阈值，初始化要匿名的属性值
    :return: 所有数据元祖，阈值，所有属性的树
    '''

    #第一步：读取数据，生成元组
    path = os.path.abspath('..')  # 表示当前所处的文件夹上一级文件夹
    data_path = path + '\\data\\data.csv'
    data_file = open(data_path, 'r')
    lines = data_file.readlines()
    for line in lines:
        i = line[:-1].split(',')
        data.append(i)


def GetNewLoss(index,data):
    '''
    根据是否是数值型的树，返回损失值
    :param tree: 属性的树
    :param attribute: 属性值
    :return: 损失率
    '''
    column = list()
    for i in range(len(data)):
        column.append(data[i][index])
    #获得单个属性的list
    data_set = set(column)

    total = 0
    for i in data_set:
        total = total - ((column.count(i)/len(data)) * math.log(column.count(i)/len(data)))
    return total

def GetNewLoss_2(data):
    #设属性集数量为3，带入为m = 3
    total = 0
    for i in range(7):
        total = total + GetNewLoss(i,data)
    result = (1 / 7)*total
    return result

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


def GetDepth(attr,data):
    depth = Trees[attr].depth(data[attr])
    return depth


def is_same(data1,data2):
    for i in range(7):
        if data1[i] != data2[i]:
            return False
    return True

if __name__ == '__main__':
    Init()
    if k < 2:
        print("参数k不能小于2")
        exit()

    print(Trees)
    lowLoss = None
    lowAttr = None
    #循环后获得最低损失的数据
    lowLoss_arr = []
    lowLossDepth_arr = []
    totalDepth_arr = []
    lowAttr_arr = []
    results = []
    totalLoss = 0
    precision = 0

    for i in range(7):
        origin_data = data[:]  # 拷贝data数据
        totaldepth = Trees[i].depth() #获得树的深度
        totalDepth_arr.append(totaldepth)
        if lowLoss == None:
            lowLoss,depth = GetAttrLoss(i,origin_data) #同时得到每个属性泛化后的深度
            totalLoss = totalLoss + lowLoss
            lowAttr = i
        else:
            tmpLoss,depth = GetAttrLoss(i,origin_data)
            totalLoss = totalLoss + tmpLoss
            if tmpLoss < lowLoss:
                lowLoss = tmpLoss
                lowAttr = i
        lowLossDepth_arr.append(depth)
        lowLoss_arr.append(lowLoss)
        lowAttr_arr.append(lowAttr)
        results.append(origin_data[:])
    #得到了损失最低的数据
    lowLoss_data = results[lowAttr]
    KN_result = []
    print(lowLoss_data)

    for i in range(len(lowLoss_data)):
        for j in range(len(lowLoss_data[i])): #遍历所有属性，重新获取当前深度
            lowLossDepth_arr[j] = GetDepth(j,lowLoss_data[i])
        break


    count = 0
    for i in range(len(lowLoss_data)):
        tmp_k = 1
        same = False
        for j in range(len(lowLoss_data)):
            if i == j:
                continue
            if is_same(lowLoss_data[i],lowLoss_data[j]):
                tmp_k = tmp_k+1
                if tmp_k >= k:
                    same = True
                    break
        count = count+1
        print("比对数据中..."+str(count))
        KN_result.append(same)
    print(KN_result)

    while False in KN_result: #不符合K匿名,继续泛化
        print("不符合K匿名,继续泛化")
        while True:
            lowLoss_index = lowLoss_arr.index(min(lowLoss_arr)) #获得最小损失的属性索引
            if lowLossDepth_arr[lowLoss_index] == 0:
                lowLoss_arr[lowLoss_index] = 99999
                #print("属性"+str(lowAttr_arr[lowLoss_index])+"深度0,无法继续泛化")
            else:#属性可以继续泛化,得到index,跳出循环
                break
        print(lowLoss_data)
        tmpLoss, depth = GetAttrLoss(lowLoss_index,lowLoss_data)
        print(lowLoss_data)
        lowLossDepth_arr[lowLoss_index] = depth #更新depth
        lowLoss_arr[lowLoss_index] = tmpLoss #更新loss
        KN_result = []
        count = 0
        for i in range(len(lowLoss_data)):
            tmp_k = 1
            same = False
            for j in range(len(lowLoss_data)):
                if i == j:
                    continue
                if is_same(lowLoss_data[i],lowLoss_data[j]):
                    tmp_k = tmp_k + 1
                    if tmp_k >= k:
                        same = True
                        break
            count = count + 1
            print("比对数据中..." + str(count))
            KN_result.append(same)

    print("成功符合K匿名")
    print(lowLoss_arr) #打印损失
    print(lowLossDepth_arr) #打印出泛化深度
    for i in range(7):
        precision = precision + (1 - (lowLossDepth_arr[i] / totalDepth_arr[i]))
    print(precision/7)
    if False not in KN_result: #符合K匿名
        Save2File(lowLoss_data)#输出结果 为data目录的output.txt文件
        

