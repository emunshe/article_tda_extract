import re

# 标题、时间配置文件
DT_INFO = {
    'date': {
        'REGEXES': re.compile('(<[^>]*?>((?!>)|(?!<).)*(20\d{2}年\d{1,2}月\d{1,2}日|20\d{2}-\d{1,2}-\d{1,2}|20\d{2}/\d{1,2}/\d{1,2}|20\d{2}\.\d{1,2}\.\d{1,2}|[0-2][0-9]-\d{1,2}|\d{1,2}月\d{1,2}日)(\d+:+\d*:*\d*|\d+时\d*分\d*|\d*:*\d*:*\d*))', re.M),
        # 'REGEXES': re.compile('(<[^>]*?>((?!>)|(?!<).)*(20\d{2})*(年|\\|-|\.)*[0-1]*[0-9][月\-/.][0-3]*[0-9]日*(\d+:+\d*:*\d*|\d+时\d*分\d*|\d*:*\d*:*\d*))', re.M),
        'LABLE': ['span', '/span', 'p', 'div', 'td', 'strong', 'em', 'time', 'i', 'h6'],
        'CSS': ['.pub_time', '.date', '.time', '#txt12', '.post_time_source', '.post-time', '#ArtFrom'],
        'LAST_REGEXES': re.compile(
           '((\d{4}-\d{1,2}-\d{1,2}|\d{4}/\d{1,2}/\d{1,2}|\d{4}年\d{1,2}月\d{1,2}日|\d{4}\.\d{1,2}\.\d{1,2}|[0-2][0-9]-\d{1,2}|\d{1,2}月\d{1,2}日)(\d+:\d*:\d*|\d+时\d*分\d*|\d*:*\d*:*\d*))',
            re.I),
    },
    'title': {
        # 'REGEXES': re.compile('(?<=<founder-title>).*?(?=</founder-title>|\n|\r|$)', re.I|re.M),
        'LABLE': ['.//h1', './/h2', './/h3', './/founder-title', './/strong'],
        'CSS': ['#title', '#head', '#heading', '.pageTitle', '.news_title',
                '.title', '.head', '.heading', '.contentheading', '.small_header_red',
                '.font01', '#APP-Title'
                ]
    },
}

# 月份对应的英文
EN_DATE = {'Jan': '1', 'Feb': '2', 'Mar': '3', 'Apr': '4', 'May': '5', 'Jun': '6',
          'Jul': '7', 'Aug': '8', 'Sep': '9', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

# 作者正则列表
AS_INFO = {
    'author': ['(?<=<founder-author>)()(\s?.*?)(?=</founder-author>|\n|\r|$)',
                '作者[：,　, ]<span.*?>()(.*?)</span>',
                '<strong>(.*?) 作者：(.*?) .*?</strong>',
                '<p>作者[：,　, ]()(\w+)</p>',
                '<span>作者[：,　, ]()(\w+).*?</span>',
                '<p class="author">(.*?)记者&nbsp;(.*?)</p>',
                '<[^>]*? class="author">()(.*?)</.*?>',
                '中青在线记者[：,　, ]()([\w,\.,\s,\，]+)',
                '(作者|本报记者|通讯员)&nbsp;&nbsp;([\w,\.,\s,\,]+)',
                '<span class="name">()(.*)</span>',
                '<strong>.*?作者：()(.*?)，原题：.*?</strong>',
                '<div align="right">(\s*)作者：\s*(.*?)　　\s*编辑：\s*.*</div>',
                '(作者|本报记者|通讯员)[：,　,]([\w,\.,\s,\，]+)',],
    'source': ['来源[：, ]<a.*?>(.*?)</a>',
                '来源[：, ].*?<span itemprop="name" class="ss03"><a .*?>(.*?)</a></span>',
                '来源[：, ].*?<span itemprop="name" class="ss03">(.*?)</span>',
                '<div class="yc_tit">[\s\S]*<a  href="http://news.cctv.com.*?" target="_blank">\s*(.*?)</a>',
                '来源[: ,：, ].*?<a.*?>(.*?)</a>',
                'content="来源：(.*?)"',
                '本文摘自：(.*?)，.*?',
                '来源[：, ]([\u4E00-\u9FA5,A-Za-z,\.,\s]+ )',
                '来源[：, ]([\w,\.,\s]+)',]
}