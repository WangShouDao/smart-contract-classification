import os
import time
import spider.spider_contracts


# 创建txt文件存储数据
def mknod(filename):
    if not os.path.exists(filename):
        fp = open(filename, 'w+')
        fp.close()
        return True
    else:
        fp = open(filename, 'w+')
        fp.truncate()
        return False

if __name__=='__main__':
    # 存储合约的主要信息
    content_filename = 'txt_file/contractVf.txt'
    # 新建存储合约的txt文件
    # mknod(content_filename)
    # 爬取合约的主要信息
    # for i in range(1, 950):
    #     spider_content(i)
    # 每天新增的合约数量的折线图
    # drawing.draw_plot1(content_filename)
    # 总的合约数量的折线图
    # drawing.draw_plot2(content_filename)
    # drawing.draw_plot3(content_filename)
    # drawing.draw_plot4(content_filename)
    # drawing.draw_scatter(content_filename)
    # 存储合约
    # contract_filename = 'txt_file/most_use_contract.txt'
    # 新建存储合约的txt文件
    # mknod(contract_filename)
    # 爬取使用次数最多的合约信息
    # spider.spider_contract.find_most_use(content_filename, contract_filename)
    starttime = time.time()
    spider.spider_contracts.extract_address_txCount(content_filename)
    endtime = time.time()
    print(starttime - endtime)