import os
import json
from urllib import request
from lxml import etree


filename = r'f:/contracts/lda/contractlib.txt'

# 提取合约目录信息中的合约地址
def extract_address():
    address_list = []
    with open(filename, 'r+') as f:
        line = f.read().strip().split('\n')
        for item in line:
            item = json.loads(item)
            address_list.append(item['address'])
    return address_list

# 根据合约的URL爬取合约的内容信息
def spider_contracts(contract_address):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
    base_url = r"https://etherscan.io/address/"
    url = base_url + contract_address + '#code'
    req = request.Request(url, headers=header)
    response = request.urlopen(req)
    html_data = response.read().decode('utf-8')
    filename = r"f:/contracts/lda/traincontract/" + contract_address + ".txt"
    parse_contract(html_data, filename)

# 解析并下载合约内容,写入到本地
def parse_contract(html_data, filename):
    page = etree.HTML(html_data)
    result = page.xpath('//pre/text()')[0]
    result.replace(u'\xa0', u' ')
    with open(filename, 'w+', encoding='utf-8',errors='ignore') as f:
        f.write(result)

if __name__=='__main__':
    address_list = extract_address()
    for address in address_list:
        spider_contracts(address)