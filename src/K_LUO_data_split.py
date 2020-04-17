
cls = ['age', 'workclass', 'fnlwgt',  'education', 'education-num', 'marital-status', 'occupation', 'relationship',
       'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'label']  # 数据属性
QID = ['age', 'workclass','education','marital-status','race','sex','native-country']

from time import sleep
import math
from model import *
import os
import pandas as pd
import time
import threading

import argparse
import platform
import sys
import multiprocessing

parser = argparse.ArgumentParser(description='K-Anonymity Demo')
parser.add_argument('--data_file', type=str, required=True,
                    help='the file name of data that need to be anonymity')
parser.add_argument('--k', type=str, required=True,
                    help='the k of k-anonymity')
parser.add_argument('--output_file', type=str, required=True,
                    help='the name of output_file, result will be stored in direction of data')

parser.add_argument('--split_chunk', type=str, required=True,
                    help='set the num of data split parts')


args = parser.parse_args()

data = []
TreeDict = GetTreesDict()
k = int(args.k)


split_chunk = int(args.split_chunk)

## 用于存储最终结果
# result =pd.DataFrame(columns=QID)
precision = 0

def Init():
    '''
    初始化，生成树,设置阈值，初始化要匿名的属性值
    :return: 所有数据元祖，阈值，所有属性的树
    '''

    #第一步：读取数据，生成元组
    path = os.path.abspath('..')  # 表示当前所处的文件夹上一级文件夹
    # data_path = path + '/data/data.csv'
    data_path = path + '/data/' + args.data_file

    data_file = open(data_path, 'r')
    lines = data_file.readlines()
    for line in lines:
        i = line[:-1].split(',')
        data.append(i)

    return data


class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def worker(name, q, tmp_data, k):
    ## 用于存储最终结果
    result = pd.DataFrame(columns=QID)
    ## 计算程序运行时间
    start = time.time()

    while True:
        #     【1】 对原始数据进行拷贝后，进行K匿名检测
        k_check_res = Test_K_Anonymity(tmp_data, QID, k)
        k_sum = sum(k_check_res)  ## 计算tmp_data 中满足 k 匿名的数据条数
        total_items = tmp_data.shape[0]
        if k_sum == total_items:
            ## 满足K匿名条件, 将数据加入到最终结果集，并停止运行
            print("进程" + name + "：满足最终K匿名，停止运算")
            result.append(tmp_data)
            break
        elif total_items <= k:  ## 数据总条数是否小于等于 K值，若是则全部泛化为最高层级，并加入最终结果集
            print("进程" + name + "：数据条数小于K，则进行最高级泛化")
            gen_data = final_generalize(TreeDict, tmp_data.columns, tmp_data)
            tmp_res = result.copy().append(gen_data)  ## 将泛化后的数据，加入到最终结果集，并判断是否满足K匿名
            tmp_check_res = Test_K_Anonymity(tmp_res, QID, k)
            tmp_sum = sum(tmp_check_res)
            if tmp_sum == tmp_res.shape[0]:  ## 若满足K匿名条件，则输出最终结果，否则不做任何处理
                result = tmp_res
                print("进程" + name + "：剩余数据进行最高级泛化后，加入最终结果集，仍然满足K匿名条件，停止运算")
            else:
                print("进程" + name + "：剩余数据进行最高级泛化后，加入最终结果集,无法满足K匿名条件，停止运算")
            break
        else:  ## 数据条数> K， 则将满足K匿名的数据条目全部抽取到最终结果后，执行第三步
            # print("数据条数 > K， 将数据集中的，满足K匿名的样本，提取到最终结果集中")

            satisfy = tmp_data.loc[k_check_res]
            result = result.append(satisfy)

            for tmp_index in range(len(k_check_res)):
                k_check_res[tmp_index] = not k_check_res[tmp_index]

            tmp_data = tmp_data.loc[k_check_res]  ## 提取后，获得提取后的数据

            '''
            第三步，属性集长度为n，选择n-1个属性组成n种集合的元组，统计出各元组中存在的等价类的个数，
            并取等价类数量最大的元组属性的补集进行泛化，所泛化的属性值是元组中等价类对应的数据项中的属性值，
            将泛化后的结果返回到第一步进行K匿名检测

            采用多线程方式，以提高处理速度
            '''

            ## 多线程的列表
            threads = []

            equil_num_list = []
            attr_k_check_res_dict = {}

            '''
            采用多线程处理
            '''
            for i in range(len(QID)):
                tmp_qid = QID.copy()
                tmp_qid.remove(QID[i])

                ## 构造线程，同时采用one-hot编码方式，速度可提升大约 n倍， n的
                t = MyThread(Test_K_Anonymity_One_Hot, (tmp_data, tmp_qid, k,), Test_K_Anonymity.__name__)
                threads.append(t)

            for i in range(len(QID)):  # start threads 此处并不会执行线程，而是将任务分发到每个线程，同步线程。等同步完成后再开始执行start方法
                threads[i].start()

            for i in range(len(QID)):  # jon()方法等待线程完成
                threads[i].join()

            for i in range(len(QID)):
                attr_k_check_res = threads[i].get_result()
                equil_num = sum(attr_k_check_res)
                equil_num_list.append(equil_num)
                attr_k_check_res_dict[i] = attr_k_check_res

            '''
            选择待泛化的属性列，规则为：
            存在等价类数据多的列，若等价类数目一样，则选择属性取值多的那一个进行泛化
            '''
            equil_max = max(equil_num_list)
            selected_attr_num = 0
            attr_num = 0
            for i in range(len(equil_num_list)):
                if equil_num_list[i] == equil_max:
                    tmp_attr_num = len(set(tmp_data[QID[i]]))  ## 如果等价类个数满足条件，则计算属性值类型个数
                    if tmp_attr_num > attr_num:
                        attr_num = tmp_attr_num
                        selected_attr_num = i

            ## 对选择的属性列进行泛化，并重新运行整个过程
            # generalize(tree_dict, gen_col, data, index_boolean)
            index_boolean = attr_k_check_res_dict[selected_attr_num]
            ## 异常情况，当所有的数据均没有等价类时，要泛化选中属性的所有样本
            if equil_max == 0:
                for tmp_index in range(len(index_boolean)):
                    index_boolean[tmp_index] = not index_boolean[tmp_index]

            tmp_data = generalize(TreeDict, QID[selected_attr_num], tmp_data, index_boolean)

            # print("泛化属性列为" + QID[selected_attr_num] + ", 泛化后的结果为：")
            # print(tmp_data)

    end = time.time()
    print('\n\n' + "进程" + name + '：泛化总运行时长为:\n' + str(end - start))
    # print('\n\n最终泛化结果如下:\n')
    # print(result)

    result.to_csv('../data/' +name + '_' + args.output_file, sep=',')  # 以竖线分隔

    # Save2File(result)
    # Save2File2(result, args.output_file)

    '''
    计算数据的损失
    '''
    total_loss = 0.0
    # total_loss_2 = 0.0
    m, n = result.shape

    # print(tmp_raw_data)

    for j in range(n):
        tree = TreeDict.get(QID[j])
        for i in range(m):
            # print(result.iloc[i][j])
            total_loss += GetLoss(tree, result.iloc[i][j])
            # total_loss_2 += GetHeightLoss(tree, result.iloc[i][j])

    # print("total_loss=" + str(total_loss))
    # print("total_loss_2=" + str(total_loss_2))

    precision_1 = 1.0 - total_loss / (m * n * 1.0)
    # precision_2 = 1.0 - total_loss_2 / (m * n * 1.0)

    # print("precision_1=" + str(precision_1))
    # print("precision_2=" + str(precision_2))

    # res_dict = {}
    #
    # res_dict['result'] = result
    # res_dict['precision'] = precision_1

    q.put(precision_1)




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

    ##【3】数据分块依据

    total_num = raw_data.shape[0]

    split_item_num = math.ceil(total_num / split_chunk)


    ## 用于存储中间结果
    q = multiprocessing.Queue()
    jobs = []
    ## 计算程序运行时间
    start = time.time()

    # 【4】并发执行不同数据分块结果
    for i in range(split_chunk):
        next = i+1
        if i == (split_chunk - 1):
            tmp_data = raw_data.iloc[(i * split_item_num):].copy()
        else:
            tmp_data = raw_data.iloc[(i * split_item_num):(next * split_item_num)].copy()

        p = multiprocessing.Process(target=worker, args=(str(i), q, tmp_data, k))
        jobs.append(p)
        p.start()

    for p in jobs:
        p.join()



    ##【5】组装最终结果
    final_precision = 0.0
    # final_result = pd.DataFrame(columns=QID)
    for p in jobs:
        final_precision += q.get()
        # tmp_dict = q.get()

        # tmp_res = tmp_dict.get('result')
        # final_precision += tmp_dict.get('precision')

        # final_result.append(tmp_res)


    end = time.time()
    print('\n\n泛化总运行时长为:\n' + str(end - start))
    print("precision=" + str(final_precision / split_chunk))

    # final_result.to_csv('../data/' + args.output_file, sep=',')  # 以竖线分隔




