# K-Anonymity



算法复杂度：(O)N方*M方

例如：7列，1000条数据

复杂度：7*7 * 1000 * 1000

### 下载Anaconda3版本

```bash
curl -# -O https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh

bash Anaconda3-2020.02-Linux-x86_64.sh

source /root/.bashrc
```



### 安装treelib

```bash
sudo easy_install -U treelib # 安装路径不对

python --version
python3 --version
pip --version

pip install pandas
pip install treelib
pip install sklearn # 增加多线程，1000条数据需要依赖
yum install python-pandas
```


```bash
wget https://github.com/JaredNie/K-Anonymity/archive/master.zip
unzip master.zip
```

### 启动脚本

```bash
cd /usr/local/src/K-Anonymity/src/

python K_LUO.py

# 后台执行
nohup python K_LUO.py >my.log &

```



**多线程版本，速度可以提升一些**

50条数据，单线程 =45s 多线程 = 6s

100条数据，单线程 =375s 多线程 = 21s

1000条数据，单线程 =5381s 多线程 = 825s



| 数据条数 | 优化前    | 多线程   |
| -------- | --------- | -------- |
| 50       | 45秒      | 6秒      |
| 100      | 375秒     | 21秒     |
| 1000     | 5381秒    | 825秒    |
| 30000    | 11081分钟 | 1457分钟 |



```bash
# 运用命令行执行， --data_file 放在data目录下的数据文件名， --k; k 匿名的k值
# --output_file  为结果的输出文件名，也是在data目录下
python K_LUO_multi_thread.py --data_file 100.txt --k 2 --output_file res_100.txt
python K_LUO_multi_thread.py --data_file 1000.txt --k 2 --output_file res_1000.txt
python K_LUO_multi_thread.py --data_file 30000.txt --k 2 --output_file res_30000.txt

# 后台执行
nohup python K_LUO_multi_thread.py --data_file 30000.txt --k 2 --output_file res_30000.txt &

```





**数据分片**



```bash
python K_LUO_multi_thread.py --data_file 100.txt --k 2 --output_file res_100.txt --split_chunk 10
```









### 跑1000条数据大约1小时


```bash
  age          workclass      education  ...    race      sex  native-country
0    39          State-gov      Bachelors  ...   White     Male   United-States
1    50   Self-emp-not-inc      Bachelors  ...   White     Male   United-States
2    38            Private        HS-grad  ...   White     Male   United-States
3    53            Private           11th  ...   Black     Male   United-States
4    28            Private      Bachelors  ...   Black   Female            Cuba
..   ..                ...            ...  ...     ...      ...             ...
995  43            Private      Bachelors  ...   White   Female   United-States
996  19          Local-gov        HS-grad  ...   White   Female   United-States
997  58   Self-emp-not-inc        HS-grad  ...   White     Male   United-States
998  41          Local-gov   Some-college  ...   White     Male   United-States
999  31            Private   Some-college  ...   White     Male    United-State
[1000 rows x 7 columns]

Traceback (most recent call last):
File "K_LUO.py", line 130, in <module>
  tmp_data = generalize(TreeDict, QID[selected_attr_num], tmp_data, index_boolean)
File "/usr/local/src/K-Anonymity-master/src/model.py", line 172, in generalize
  tmp_attribute = climb(tree, data.loc[index][gen_col])  # 得到父节点
File "/usr/local/src/K-Anonymity-master/src/model.py", line 141, in climb
  return (tree.parent(attribute).tag)  # 返回父节点
File "/usr/local/src/anaconda3/lib/python3.7/site-packages/treelib/tree.py", line 596, in parent
  raise NodeIDAbsentError("Node '%s' is not in the tree" % nid)
treelib.exceptions.NodeIDAbsentError: Node ' United-State' is not in the tree

```
