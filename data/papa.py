import pandas as pd
import numpy as np
from sklearn import preprocessing
def Init():
    cls = ['age', 'workclass', 'education', 'marital-status', 'race', 'sex', 'native-country']  # 数据属性
    cols = ['workclass', 'education','marital-status', 'race', 'sex', 'native-country']
    path = "2.13/K值 和 output/K-Anonymity-master/data/data.csv"
    data = pd.read_csv('data.csv', header=None, names=cls, index_col=False)
    lbl = preprocessing.LabelEncoder()
    for col in cols:
        data[col] = lbl.fit_transform(data[col])
    return data
'''K匿名函数'''
def if_K(data):
    a = []
    a.append(data[0, :])
    cou_a = []
    cou_a.append(1)
    ind_a = []
    ind_a.append(0)
    for i in range(1, len(data)):
        flg = 1
        for j in range(len(a)):
            if sum(abs(data[i, :]-a[j])) == 0:
                cou_a[j] = cou_a[j] + 1
                ind_a.append(j)
                flg = 0
                break
        if flg == 1:
            ind_a.append(len(a))
            a.append(data[i, :])
            cou_a.append(1)
    c = []
    for i in range(len(ind_a)):
        c.append(cou_a[ind_a[i]])

    return c
'''判断数据集是否满足K匿名'''
def dataset_K(data,ind_K):
    a = if_K(data)
    if min(a) >= ind_K:
        return True
    else:
        return False
test = Init().values
def if_process():
    pass
def DisRate(data):
    da = data.values.transpose()
    list1 = [da[i] for i in range(len(da))]
    list2 = [len(pd.Series(list1[j]).unique()) for j in range(len(da))]
    return list2
