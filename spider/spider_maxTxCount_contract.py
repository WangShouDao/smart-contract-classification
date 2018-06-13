# -*- coding:utf-8 -*-
import os
import json
from urllib import request
from lxml import etree

# 寻找使用次数最多的合约
def find_most_use(filename, filename2):
    with open(filename, 'r+') as f:
        line = f.read().strip().split('\n')
        max_use = 0
        address_txCount = {}
        contract_address = ''
        for item in line:
            item = json.loads(item)
            if max_use < int(item['txCount']):
                max_use = int(item['txCount'])
                contract_address = item['address']
    frequent_contract(address_txCount)
    # print(max_use, contract_address)

# 爬取使用次数最多的合约
def spider_most_use(contract_address, filename2):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
    base_url = r"https://etherscan.io/address/"
    url = base_url + contract_address + '#code'
    print(url)
    req = request.Request(url, headers=header)
    response = request.urlopen(req)
    html_data = response.read().decode('utf-8')
    parse_contract(html_data, filename2)

# 解析并下载合约内容
def parse_contract(html_data, filename2):
    page = etree.HTML(html_data)
    result = page.xpath('//pre/text()')[0]
    with open(filename2, 'w+') as f:
        f.write(result)