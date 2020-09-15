from tdaExtract.config import DT_INFO, EN_DATE
from tdaExtract.cleaners import norm_title
from tdaExtract.encoding import get_encoding
from tdaExtract.specialURL import last_getdate
import lxml.html
import time
import re

utf8_parser = lxml.html.HTMLParser(encoding='utf-8')


# def distance_scoring(html, title, info_match):
#     title_position = html.find(re.sub('\s', '', title))


def get_date(clean_html, html, response_url, doc_html=None, title=None, header_time=None):
    """
    Return a dictionary with date and timestamp
    clean_html -- clear html
    html -- original html
    response_url -- URL
    """
    info_heuristics = DT_INFO['date']
    candidates = {}                 # 储存分数的字典
    position_tulpe = ()             # 存储时间与标题距离的元祖
    title_position = 0              # 标题在html中的位置，默认为0
    info_matchs = info_heuristics['REGEXES'].findall(clean_html)
    num = len(info_matchs)
    if info_matchs:
        if title:
            title_position = clean_html.find(re.sub('\s', '', title))    # 获取title的位置
        for info_match in info_matchs:
            info_match = info_match[0]
            info_position = clean_html.find(info_match)         # 获取info_match的位置
            position = abs(title_position-info_position)        # 获取info_match与title的距离
            if not position_tulpe:
                position_tulpe = (info_match, position)
            elif position < position_tulpe[1]:                  # title位置小于上一个info位置则替换
                position_tulpe = (info_match, position)
            if info_match[0] in candidates:
                continue
            candidates[info_match] = num * 0.25
            num -= 1
            for key in info_heuristics['LABLE']:
                if '<' + key in info_match or key.upper() in info_match:
                    add_match(candidates, info_match, 0.4)
                    break
        if position_tulpe:
            candidates[position_tulpe[0]] += 1
        # if header_time:
        #     ht_list = header_date_format(str(header_time))
        #     for item in candidates.keys():
        #         if ht_list[0] in item and ht_list[1] in item and ht_list[2] in item:
        #             candidates[item] += 0.2

        for css_attribute in info_heuristics['CSS']:
            css_item = 'class="%s"' % css_attribute[1:] if css_attribute[0] == '.' else 'id="%s"' % css_attribute[1:]
            for item in candidates.keys():
                if css_item in item:
                    add_match(candidates, item, 0.3)
    if candidates:
        sorted_candidates = sorted(
            candidates.items(),
            key=lambda item: item[1],
            reverse=True
        )
        for i in range(0, 2 if len(candidates) > 1 else 1):
            info_key = sorted_candidates[i][0]
            result = get_realDate(info_key)
            if result:
                return result
        info_key = last_getdate(html, response_url)
        return get_realDate(info_key) if info_key else {'publishDateStr': '', 'publishDate': ''}

    else:
        info_key = last_getdate(html, response_url)
        return get_realDate(info_key) if info_key else {'publishDateStr': '', 'publishDate': ''}


def header_date_format(res_header):
    """
    转换响应头时间格式
    :param res_header:
    :return: date_lstt
    """
    date_list = res_header.split(" ")
    if date_list:
        dy, dm, dd = date_list[3], date_list[2], date_list[1]
        for key in EN_DATE.keys():
            if dm == key:
                if int(date_list[4][:2]) > 24:
                    dd += 1
                header_time_list = [dy, EN_DATE[dm], dd]
                return header_time_list
    else:
        return ''


def add_match(candidates, text, score=0.0):
    """
    加分
    :param candidates:
    :param text:
    :param score:
    :return:
    """
    if text in candidates.keys():
        candidates[text] += score
    else:
        candidates[text] = score


def get_realDate(str_info):
    """
    取出加权后最高分的时间并转换为UTC时间
    :param str_info:
    :return:
    """
    detail_regexes = DT_INFO['date']['LAST_REGEXES']
    date = detail_regexes.search(str_info).group(0)
    now_time = int(time.time())
    timeArray = time.localtime(now_time)
    if '-' not in date:
        for fh in ['/', '年', '月', '.']:
            if fh in date:
                date = date.replace(fh, '-')
        for sh in ['时', '分']:
            if sh in date:
                date = date.replace(sh, ':')
        for nh in ['日', '秒']:
            if nh in date:
                date = date.replace(nh, '')
    colol = date.count(':')
    try:
        if colol:
            if colol == 1:
                if date.endswith(':', -1):
                    date = date+'00:00'
                else:
                    date = date+':00'
            if date.endswith(':', -1):
                date = date+'00'
            gap_num = date.find(':') - date.rfind('-')-1
            s_p = date.find(':') - 2 if gap_num == 4 else date.find(':') - 1
            return tf_timestamp(date[:s_p] + ' ' + date[s_p:])
        else:
            return tf_timestamp(date+' '+time.strftime("%H:%M:%S", timeArray))
    except:
        return None


def tf_timestamp(dt_time):
    """
    为没有年份的日期加上当前年份，并转换时间戳
    """
    if len(dt_time) == 14 or len(dt_time) == 15:
        dt_time = time.strftime("%Y")+'-'+dt_time
    timeArray = time.strptime(dt_time, '%Y-%m-%d %H:%M:%S')
    timeStamp = time.mktime(timeArray)
    if timeStamp > time.time():
        return None
    publishDateStr = dt_time.replace(' ', 'T') + ' 0800'
    return {'publishDateStr': publishDateStr, 'publishDate': timeStamp}


def get_title(doc, html):
    """
    获取标题
    :param doc:
    :param html:
    :return:
    """
    title = doc.find('.//title')
    if title is None or title.text is None or not title.text.strip():
        t1 = re.search(r'<title>(.*?)</title>', re.sub(r'\s', '', html)).group(0)
        title = re.sub(r'</?\w+[^>]*>', '', t1)
    else:
        title = title.text
    title = orig = norm_title(title)
    for delimiter in [' | ', ' - ', ' :: ', ' / ', '_', '·', '-']:
        if delimiter in title:
            parts = orig.split(delimiter)
            # value = ''
            # for pt in parts:
            #     if len(pt) > len(value):
            #         value = pt
            # title = value
            if len(parts[0]) >= 4:
                title = parts[0]
                break
            elif len(parts[-1]) >= 4:
                title = parts[-1]
                break
    if ': ' in title:
        parts = orig.split(': ')
        if len(parts[-1].split()) >= 4:
            title = parts[-1]
        else:
            title = orig.split(': ', 1)[1]

    info_title = get_info(doc, orig)
    if info_title:
        title = info_title if len(info_title) > 15 or info_title in orig or len(info_title) >= len(title) else title
    if not title:
        title = ''
    return {'title': title}


def get_info(doc, title):
    """
    对标题进行启发式规则查找
    :param doc:
    :param html_text:
    :return:
    """
    info_heuristics = DT_INFO['title']
    candidates = {}
    # score = lambda x: 2 if item == './/founder-title' else 1
    for item in info_heuristics['LABLE']:
        for e in list(doc.iterfind(item)):
            if e.text:
                if e.text in title:
                    add_match(candidates, e.text, 3)
                else:
                    add_match(candidates, e.text, 1)
            else:
                continue
            # if e.text_content():
            #     add_match(candidates, e.text_content(), score(item))

    for item in info_heuristics['CSS']:
        for e in doc.cssselect(item):
            if e.text:
                if e.text in title:
                    add_match(candidates, e.text, 3)
                else:
                    add_match(candidates, e.text, 1)
            else:
                continue
    if candidates:
        sorted_candidates = sorted(
            candidates.items(),
            key=lambda item: item[1],
            reverse=True
        )
        info_key = norm_title(sorted_candidates[0][0])

        return info_key
    else:
        return ''


def build_doc(page):
    """
    构建dom树
    :param page:
    :return:
    """
    if isinstance(page, str):
        encoding = None
        decoded_page = page
    else:
        encoding = get_encoding(page) or 'utf-8'
        decoded_page = page.decode(encoding, 'replace')

    # XXX: we have to do .decode and .encode even for utf-8 pages to remove bad characters
    doc = lxml.html.document_fromstring(decoded_page.encode('utf-8', 'replace'), parser=utf8_parser)
    return doc, decoded_page, encoding

