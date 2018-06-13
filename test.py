import os
import re

def remove_annote():
    # filepath1 = r'F:\contracts\contracts_origin\30793-0x107c4504cd79c5d2696ea0030a8dd4e92601b82e.txt'
    filepath1 = r'F:\tttt.txt'
    filepath2 = r'F:\tet.txt'
    # filepath2 = r'F:\contracts\contract_clear\1-0x000000002647e16d9bab9e46604d75591d289277.txt'
    # result = []
    with open(filepath1, 'r+', encoding='utf-8') as f:
        with open(filepath2, 'w+', encoding='utf-8') as f1:
            flag = 0
            for line in f.readlines():
                line = line.strip()
                if flag == 0:
                    if '/*' in line:
                        flag =1
                        continue
                    if not len(line) or '*' in line or line.startswith('pragma') or '//' in line:
                        continue
                if flag == 1:
                    if '*/' in line:
                        flag = 0
                    continue
                f1.write(line)
                f1.write('\n')

if __name__=='__main__':
    remove_annote()