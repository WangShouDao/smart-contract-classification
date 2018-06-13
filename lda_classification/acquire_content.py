# -*- coding:utf-8 -*-
import json
import os
from urllib import request
from lxml import etree

# 存放合约的相关信息
contractlib = r'f:/contracts/lda/contractlib.txt'

# 爬取每个页面
def spider_content(i):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
    base_url = r"https://etherscan.io/contractsVerified/"
    offset = i
    url = base_url + str(offset)
    req = request.Request(url, headers=header)
    response = request.urlopen(req)
    html_data = response.read().decode('UTF-8')
    parse(html_data)

# 解析每个页面，把每个合约的信息提取出来
def parse(html_data):
    # soup = bs(html_data, 'lxml')
    page = etree.HTML(html_data)
    for each in page.xpath('//tbody'):
        for field in each.xpath('./tr'):
            contractVf = {}
            contractVf['address'] = field.xpath('./td[1]/a/text()')[0]
            contractVf['cname'] = field.xpath('./td[2]/text()')[0]
            contractVf['complier'] = field.xpath('./td[3]/text()')[0]
            contractVf['balance'] = field.xpath('./td[4]/text()')[0]
            contractVf['txCount'] = field.xpath('./td[5]/text()')[0]
            contractVf['dateVf'] = field.xpath('./td[7]/text()')[0]
            write(contractVf)

# 把每条记录写入文本文件
def write(contractVf):
    with open(contractlib, 'a+') as f:
        f.write(json.dumps(contractVf) + '\n')


# 创建txt文件存储数据
def mkdir(filename):
    if not os.path.exists(filename):
        fp = open(filename, 'w+')
        fp.close()
        return True
    else:
        fp = open(filename, 'w+')
        fp.truncate()
        return False

if __name__=='__main__':
    mkdir(contractlib)
    for i in range(751, 769):
        spider_content(i)