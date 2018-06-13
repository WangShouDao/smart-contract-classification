import re
from matplotlib import pyplot as plt
import numpy as np

def count_function(filepath):
    try:
        i = 0
        function_dict = {}
        with open(filepath, 'r+') as f:
            line = f.readline().strip()
            while len(line)!=0:
                if 'Function' in line:
                    item = re.split(':', line)[1].strip()
                    function = re.split('\(', item)[0].strip()
                    if function not in function_dict.keys():
                        function_dict[function] = 1
                    else:
                        function_dict[function] += 1
                line = f.readline().strip()
                i = i+1
                print(i, function_dict)
        return function_dict
    except Exception as e:
        return None

def draw(function_dict):
    name = []
    count = []
    for (k,v) in function_dict.items():
        name.append(k)
        count.append(int(v))
    # 设置matplotlib正常显示中文和负号
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    bar_width = 0.3
    rects1 = plt.bar(range(len(count)), count, width=0.5, color='b')
    plt.xticks(range(len(count)), name)
    plt.xlabel('功能名称')
    plt.ylabel('功能的使用次数')
    for rect in rects1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
    plt.show()

if __name__ == '__main__':
    filepath = 'F:/python/etherscan/transactions/0x6090a6e47849629b7245dfa1ca21d94cd15878ef.txt'
    function_dict = count_function(filepath)
    draw(function_dict)
