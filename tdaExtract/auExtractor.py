from tdaExtract.config import AS_INFO
import re


def get_author(html_text):
    """
    对文章作者匹配查找
    :param html_text:
    :return:
    """
    info_heuristics = AS_INFO['author']
    as_dict = {}
    for item in info_heuristics:
        ret = parse_html(item, html_text, 'author')
        if ret:
            as_dict['author'] = ret
            break
    if as_dict and len(as_dict.get('author')) < 8:
        return as_dict
    info_heuristics = AS_INFO['source']
    for item in info_heuristics:
        ret = parse_html(item, html_text, 'source')
        if ret:
            as_dict['author'] = ret
            break
    if as_dict and len(as_dict.get('author')) < 8:
        return as_dict
    else:
        as_dict['author'] = ''
        return as_dict


def parse_html(regex, html, style):
    try:
        if style == 'author':
            ret = re.search(regex,html).group(2)
        if style == 'source':
            ret = re.search(regex, html).group(1)
    except Exception:
        return ""
    else:
        return ret