from tdaExtract.dtObtain import Document
import requests, json, redis, pymongo, time
import hashlib, re

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}


def get_html(url):
    try:
        start_time = time.time()
        response = requests.get(url, headers=header, timeout=5)
        print('请求时间：' + str((time.time() - start_time) * 1000))
        html = response.content

        item = Document(html, response.url)
        start_time = time.time()
        result = item.together()
        print('解析时间：'+str((time.time()-start_time)*1000))
        return result

    except:
        print(url+'...无法访问')


def produce_mid(url):
    mid = hashlib.md5()
    mid.update(url.encode('utf8'))
    return mid.hexdigest()


if __name__ == "__main__":
    url = 'https://wallstreetcn.com/vip/articles/3440500'
    print(get_html(url))
