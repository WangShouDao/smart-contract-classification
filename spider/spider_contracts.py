import os
import json
from urllib import request
from lxml import etree

# 提取合约的地址和使用次数
def extract_address_txCount(filename):
    with open(filename, 'r+') as f:
        line = f.read().strip().split('\n')
        address_txCount = {}
        for item in line:
            item = json.loads(item)
            if int(item['txCount'])>0:
                address_txCount[item['address']] = int(item['txCount'])
    sort_contract(address_txCount)

# 对合约地址按使用次数排序
def sort_contract(d):
    d=sorted(d.items(), key=lambda x: x[1],reverse=True)
    with open('txt_file/address_txCount.txt', 'w+') as f:
        for i in range(len(d)):
            f.write(d[i][0]+ ':' + str(d[i][1]) + '\n')
    for i in range(len(d)):
        spider_contracts(d[i][0], d[i][1])

# 依次爬取每个合约的具体内容
def spider_contracts(contract_address):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
    base_url = r"https://etherscan.io/address/"
    url = base_url + contract_address + '#code'
    req = request.Request(url, headers=header)
    response = request.urlopen(req)
    html_data = response.read().decode('utf-8')
    filename = r"f:/python/etherscan/contracts/" +  contract_address + ".txt"
    # filename = r"f:/contracts/lda/contract/" + contract_address + ".txt"
    parse_contract(html_data, filename)

# 解析并下载合约内容
def parse_contract(html_data, filename):
    page = etree.HTML(html_data)
    result = page.xpath('//pre/text()')[0]
    result.replace(u'\xa0', u' ')
    with open(filename, 'w+', encoding='utf-8',errors='ignore') as f:
        f.write(result)