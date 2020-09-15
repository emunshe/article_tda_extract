from lxml.html.clean import Cleaner


def norm_title(title):
    return normalize_entities(normalize_spaces(title))


def normalize_eninfos(text):
    eninfos = {
        u'&nbsp':' ',
        u'&quot;': '"',
        '\r\n':'',
        '■':''
    }
    for c, r in eninfos.items():
        if c in text:
            text = text.replace(c, r)
    return text


def normalize_spaces(s):
    if not s:
        return ''
    """replace any sequence of whitespace
    characters with a single space"""
    return ' '.join(s.split())


html_cleaner = Cleaner(scripts=True, javascript=True, comments=True,
                  style=True, links=True, meta=False, add_nofollow=False,
                  page_structure=False, processing_instructions=True, embedded=False,
                  frames=False, forms=False, annoying_tags=False, remove_tags=None,
                  remove_unknown_tags=False, safe_attrs_only=False)


def normalize_entities(cur_title):
    entities = {
        u'\u2014':'-',
        u'\u2013':'-',
        u'&mdash;': '-',
        u'&ndash;': '-',
        u'\u00A0': ' ',
        u'\u00AB': '"',
        u'\u00BB': '"',
        u'&quot;': '"',
    }
    for c, r in entities.items():
        if c in cur_title:
            cur_title = cur_title.replace(c, r)
    return cur_title