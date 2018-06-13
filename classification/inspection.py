import os
path = 'F:\python\contracts'

# 读取所有的文件名
def fileList():
    file_list = []
    for file in os.listdir(path):
        file_list.append(file)
    return file_list

# 检查相同的代码
def checkRepeat(file_list):
    n = len(file_list)
    repeat_list = []
    for i in range(n):
        if file_list[i] in repeat_list:
            continue
        else:
            filepath1 = os.path.join(path, file_list[i])
            contract1 = readContract(filepath1)
            for j in range(i+1, n):
                filepath2 = os.path.join(path, file_list[j])
                contract2 = readContract(filepath2)
                if contract2 == contract1:
                    repeat_list.append(file_list[j])
    for file in repeat_list:
        os.remove(os.path.join(path, file))


# 读取合约内容
def readContract(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        contract = f.read()
    return contract

if __name__=='__main__':
    file_list = fileList()
    checkRepeat(file_list)