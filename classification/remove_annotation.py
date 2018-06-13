import os

# 获取当前目录下的非目录文件
def listdir():
    path = 'F:\\contracts\contracts_origin'
    file_list = []
    for file in os.listdir(path):
        # file_path = os.path.join(path, file)
        file_list.append(file)
    return file_list


# 清楚空格和注释
def remove_annote(file_list):
    path1 = r'F:\contracts\contracts_origin'
    path2 = r'F:\contracts\contract_clear'
    for file in file_list:
        filepath1 = os.path.join(path1, file)
        filepath2 = os.path.join(path2, file)
        with open(filepath1, 'r+', encoding='utf-8') as f:
            with open(filepath2, 'w+', encoding='utf-8') as f1:
                flag = 0
                for line in f.readlines():
                    line = line.strip()
                    if flag == 0:
                        if '/*' in line:
                            flag = 1
                            continue
                        if not len(line) or '*' in line or line.startswith('pragma') or '//' in line:
                            continue
                    if flag == 1:
                        if '*/' in line:
                            flag = 0
                        continue
                    f1.write(line)

if __name__=='__main__':
    remove_annote(listdir())
