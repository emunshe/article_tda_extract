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

# client = pymongo.MongoClient('118.244.212.178', 47017)
# # 连接所需数据库,test为数据库名
# db = client.spider
# db.authenticate('spiderteam', 'wodespider2018')
# my_set = db.nullcontent
# # 连接所用集合
# # small = myset.find({'title': {'$exists': True}, '$where': "(this.title.length < 7)"})
# # small = db.content.find({'title': re.compile('Î')})
# # small = db.content.find({'title': {'$type':'object'}})
# # small = db.content.find({'title': '48小时点击排行'})
# small = my_set.find({'is_regular_content_url': False, 'null_publishDateStr': True})
#
# num = 1
# for item in small:
#     try:
#         id = item['_id']
#         url = item['url']
#         response = requests.get(url, headers=header)
#         updata = Document(response.content, response.url).together()
#         if not updata['publishDateStr']:
#             print(url)
#             continue
#         print(id, updata)
#         db.content.update({'_id': id}, {'$set': {'title': updata['title'],
#                                                       'publishDateStr': updata['publishDateStr'],
#                                                       'publishDate': updata['publishDate']}})
#         print('success update %s'% num)
#         my_set.delete_one({'_id': id})
#         print('success delete %s' % num)
#         num += 1
#     except:
#         print('Extractor filed ----------------------')
