from lxml import etree
from urllib.parse import urlparse
import time
import re


def last_getdate(html, url):
    try:
        domain = urlparse(url)[1]
        return special_domain[domain](html)
    except:
        return None


# 定义特殊处理域名的提取函数
def newqq(html):
    d1 = re.search(r'"pubtime": "(.*)"', html).group(1)
    date = re.sub(r'\s', '', d1)
    return date


def asiafinance(html):
    domtree = etree.HTML(html)
    d1 = domtree.xpath("//span[@class='mr30'][1]/text()")[0][0]
    x = time.localtime(int(time.time())-int(d1)*24*60*60)
    date = time.strftime('%Y-%m-%d %H:%M:%S', x)
    return date


def gscncomcn(html):
    domtree = etree.HTML(html)
    d1 = domtree.xpath("//span[@class='m-frt']/text()")[0]
    date = '20'+ re.sub(r'\s', '', d1)
    return date

# 特殊域名的处理字典
special_domain = {
    'new.qq.com': newqq,
    'www.asiafinance.cn': asiafinance,
    'www.gscn.com.cn': gscncomcn,
}
